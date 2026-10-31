"""
Stimulus renderer using Pillow and NumPy.

Renders parameterized visual stimuli as static PNG images.
All rendering is deterministic given the same seed and parameters.
"""

import io
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

from mirageforge.stimuli.dsl import (
    ContrastParams,
    CrowdingParams,
    GratingParams,
    LineContextParams,
    SizeContextParams,
    StimulusFamily,
    StimulusSpec,
)
from mirageforge.utils.hashing import hash_bytes


class StimulusRenderer:
    """
    Renders visual stimuli as PNG images.

    All rendering is deterministic and reproducible given the same
    stimulus specification and seed.
    """

    def __init__(self, image_size: int = 1024):
        """
        Initialize renderer.

        Args:
            image_size: Output image size (square, in pixels)
        """
        self.image_size = image_size

    def render(self, spec: StimulusSpec) -> Image.Image:
        """
        Render a stimulus specification to an image.

        Args:
            spec: Stimulus specification

        Returns:
            PIL Image object
        """
        # Dispatch to family-specific renderer
        if spec.family == StimulusFamily.SIZE_CONTEXT:
            assert isinstance(spec.params, SizeContextParams)
            return self._render_size_context(spec.params, spec.seed)
        elif spec.family == StimulusFamily.LINE_CONTEXT:
            assert isinstance(spec.params, LineContextParams)
            return self._render_line_context(spec.params, spec.seed)
        elif spec.family == StimulusFamily.CONTRAST:
            assert isinstance(spec.params, ContrastParams)
            return self._render_contrast(spec.params, spec.seed)
        elif spec.family == StimulusFamily.CROWDING:
            assert isinstance(spec.params, CrowdingParams)
            return self._render_crowding(spec.params, spec.seed)
        elif spec.family == StimulusFamily.GRATING:
            assert isinstance(spec.params, GratingParams)
            return self._render_grating(spec.params, spec.seed)
        else:
            raise ValueError(f"Unknown stimulus family: {spec.family}")

    def render_to_file(self, spec: StimulusSpec, output_path: Path) -> str:
        """
        Render a stimulus and save to file.

        Args:
            spec: Stimulus specification
            output_path: Output file path

        Returns:
            SHA256 checksum of the saved file
        """
        image = self.render(spec)

        # Ensure output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Save as PNG without metadata
        image.save(output_path, format="PNG", optimize=True)

        # Calculate checksum
        with open(output_path, "rb") as f:
            checksum = hash_bytes(f.read())

        return checksum

    def render_to_bytes(self, spec: StimulusSpec) -> tuple[bytes, str]:
        """
        Render a stimulus to bytes.

        Args:
            spec: Stimulus specification

        Returns:
            Tuple of (PNG bytes, SHA256 checksum)
        """
        image = self.render(spec)

        # Save to bytes
        buffer = io.BytesIO()
        image.save(buffer, format="PNG", optimize=True)
        png_bytes = buffer.getvalue()

        # Calculate checksum
        checksum = hash_bytes(png_bytes)

        return png_bytes, checksum

    def _render_size_context(self, params: SizeContextParams, seed: int) -> Image.Image:
        """Render size context stimulus (Ebbinghaus-like)."""
        rng = np.random.default_rng(seed)

        # Create image
        img = Image.new("RGB", (self.image_size, self.image_size), params.background_color)
        draw = ImageDraw.Draw(img)

        center_x = self.image_size // 2
        center_y = self.image_size // 2

        # Draw context circles
        for i in range(params.num_context):
            angle = (2 * np.pi * i) / params.num_context
            # Add small random offset for natural appearance
            offset = rng.uniform(-5, 5, size=2)
            x = center_x + int(params.context_distance * np.cos(angle)) + int(offset[0])
            y = center_y + int(params.context_distance * np.sin(angle)) + int(offset[1])

            # Draw context circle
            radius = int(params.context_size / 2)
            draw.ellipse(
                [x - radius, y - radius, x + radius, y + radius],
                fill=params.context_color,
                outline=None,
            )

        # Draw target circle
        target_radius = int(params.target_size / 2)
        draw.ellipse(
            [
                center_x - target_radius,
                center_y - target_radius,
                center_x + target_radius,
                center_y + target_radius,
            ],
            fill=params.target_color,
            outline=None,
        )

        return img

    def _render_line_context(self, params: LineContextParams, seed: int) -> Image.Image:
        """Render line context stimulus (Müller-Lyer-like)."""
        img = Image.new("RGB", (self.image_size, self.image_size), params.background_color)
        draw = ImageDraw.Draw(img)

        center_x = self.image_size // 2
        center_y = self.image_size // 2

        # Draw main line
        line_start_x = center_x - int(params.line_length / 2)
        line_end_x = center_x + int(params.line_length / 2)

        draw.line(
            [(line_start_x, center_y), (line_end_x, center_y)],
            fill=params.line_color,
            width=int(params.line_width),
        )

        # Draw arrows/fins
        arrow_angle_rad = np.radians(params.arrow_angle)

        if params.arrow_type == "inward":
            # Inward arrows (like Müller-Lyer inward)
            for x in [line_start_x, line_end_x]:
                sign = 1 if x == line_start_x else -1
                dx = int(params.arrow_length * np.cos(arrow_angle_rad)) * sign
                dy = int(params.arrow_length * np.sin(arrow_angle_rad))

                draw.line(
                    [(x, center_y), (x + dx, center_y - dy)],
                    fill=params.line_color,
                    width=int(params.line_width),
                )
                draw.line(
                    [(x, center_y), (x + dx, center_y + dy)],
                    fill=params.line_color,
                    width=int(params.line_width),
                )

        elif params.arrow_type == "outward":
            # Outward arrows (like Müller-Lyer outward)
            for x in [line_start_x, line_end_x]:
                sign = -1 if x == line_start_x else 1
                dx = int(params.arrow_length * np.cos(arrow_angle_rad)) * sign
                dy = int(params.arrow_length * np.sin(arrow_angle_rad))

                draw.line(
                    [(x, center_y), (x + dx, center_y - dy)],
                    fill=params.line_color,
                    width=int(params.line_width),
                )
                draw.line(
                    [(x, center_y), (x + dx, center_y + dy)],
                    fill=params.line_color,
                    width=int(params.line_width),
                )

        # neutral: no arrows

        return img

    def _render_contrast(self, params: ContrastParams, seed: int) -> Image.Image:
        """Render simultaneous contrast stimulus."""
        img = Image.new("RGB", (self.image_size, self.image_size), "#808080")
        draw = ImageDraw.Draw(img)

        center_x = self.image_size // 2
        center_y = self.image_size // 2

        # Convert luminance to RGB
        surround_rgb = self._luminance_to_rgb(
            params.surround_luminance, params.hue, params.saturation
        )
        target_rgb = self._luminance_to_rgb(params.target_luminance, params.hue, params.saturation)

        # Draw surround
        surround_half = int(params.surround_size / 2)
        draw.rectangle(
            [
                center_x - surround_half,
                center_y - surround_half,
                center_x + surround_half,
                center_y + surround_half,
            ],
            fill=surround_rgb,
        )

        # Draw target
        target_half = int(params.target_size / 2)
        draw.rectangle(
            [
                center_x - target_half,
                center_y - target_half,
                center_x + target_half,
                center_y + target_half,
            ],
            fill=target_rgb,
        )

        return img

    def _render_crowding(self, params: CrowdingParams, seed: int) -> Image.Image:
        """Render crowding/flanking stimulus."""
        rng = np.random.default_rng(seed)

        img = Image.new("RGB", (self.image_size, self.image_size), "#FFFFFF")
        draw = ImageDraw.Draw(img)

        center_x = self.image_size // 2
        center_y = self.image_size // 2

        # Draw target
        self._draw_shape(
            draw, params.target_type, center_x, center_y, params.target_size, params.target_rotation
        )

        # Draw flankers
        if params.flanker_type != "none":
            for i in range(params.num_flankers):
                angle = (2 * np.pi * i) / params.num_flankers
                x = center_x + int(params.flanker_distance * np.cos(angle))
                y = center_y + int(params.flanker_distance * np.sin(angle))

                # Determine flanker type
                if params.flanker_type == "same":
                    flanker_shape = params.target_type
                    flanker_rotation = params.target_rotation
                else:  # different
                    # Random rotation for different flankers
                    flanker_shape = params.target_type
                    flanker_rotation = params.flanker_rotation + rng.uniform(-30, 30)

                self._draw_shape(draw, flanker_shape, x, y, params.target_size, flanker_rotation)

        return img

    def _render_grating(self, params: GratingParams, seed: int) -> Image.Image:
        """Render grating detection stimulus."""
        # Create coordinate grids
        x = np.linspace(-1, 1, self.image_size)
        y = np.linspace(-1, 1, self.image_size)
        X, Y = np.meshgrid(x, y)

        # Rotate coordinates
        theta = np.radians(params.orientation)
        X_rot = X * np.cos(theta) + Y * np.sin(theta)

        # Create grating
        phase_rad = np.radians(params.phase)
        grating = np.sin(2 * np.pi * params.spatial_frequency * X_rot + phase_rad)

        # Apply contrast
        grating = grating * params.contrast

        # Apply aperture
        if params.envelope == "gaussian":
            sigma = params.aperture_size / (2 * self.image_size)
            R = np.sqrt(X**2 + Y**2)
            aperture = np.exp(-(R**2) / (2 * sigma**2))
            grating = grating * aperture
        elif params.envelope == "circular":
            R = np.sqrt(X**2 + Y**2)
            aperture_radius = params.aperture_size / self.image_size
            aperture = (R <= aperture_radius).astype(float)
            grating = grating * aperture
        # square: no aperture

        # Convert to image
        grating = (grating + 1) / 2  # Normalize to [0, 1]
        grating = (grating * 255).astype(np.uint8)

        img_array = np.stack([grating, grating, grating], axis=2)
        img = Image.fromarray(img_array, mode="RGB")

        return img

    def _draw_shape(
        self,
        draw: ImageDraw.ImageDraw,
        shape: str,
        x: int,
        y: int,
        size: float,
        rotation: float,
    ) -> None:
        """Draw a simple shape."""
        half_size = int(size / 2)

        if shape == "square":
            draw.rectangle(
                [x - half_size, y - half_size, x + half_size, y + half_size],
                fill="#000000",
            )
        elif shape == "T":
            # T-shape
            bar_height = int(size * 0.2)
            stem_width = int(size * 0.2)

            # Top bar
            draw.rectangle(
                [x - half_size, y - half_size, x + half_size, y - half_size + bar_height],
                fill="#000000",
            )
            # Stem
            draw.rectangle(
                [
                    x - stem_width // 2,
                    y - half_size + bar_height,
                    x + stem_width // 2,
                    y + half_size,
                ],
                fill="#000000",
            )
        elif shape == "L":
            # L-shape
            bar_width = int(size * 0.2)

            # Vertical bar
            draw.rectangle(
                [x - half_size, y - half_size, x - half_size + bar_width, y + half_size],
                fill="#000000",
            )
            # Horizontal bar
            draw.rectangle(
                [x - half_size, y + half_size - bar_width, x + half_size, y + half_size],
                fill="#000000",
            )
        elif shape == "+":
            # Plus sign
            bar_width = int(size * 0.2)

            # Vertical bar
            draw.rectangle(
                [x - bar_width // 2, y - half_size, x + bar_width // 2, y + half_size],
                fill="#000000",
            )
            # Horizontal bar
            draw.rectangle(
                [x - half_size, y - bar_width // 2, x + half_size, y + bar_width // 2],
                fill="#000000",
            )

    def _luminance_to_rgb(self, luminance: float, hue: float, saturation: float) -> str:
        """Convert luminance and color to RGB hex string."""
        if saturation == 0 or hue == 0:
            # Grayscale
            value = int(luminance * 255)
            return f"#{value:02x}{value:02x}{value:02x}"
        else:
            # Chromatic (simplified HSV to RGB)
            import colorsys

            hue_norm = hue / 360.0
            r, g, b = colorsys.hsv_to_rgb(hue_norm, saturation, luminance)
            r_int = int(r * 255)
            g_int = int(g * 255)
            b_int = int(b * 255)
            return f"#{r_int:02x}{g_int:02x}{b_int:02x}"
