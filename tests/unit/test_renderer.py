"""
Unit tests for stimulus renderer.
"""

import tempfile
from pathlib import Path

import pytest
from PIL import Image

from mirageforge.stimuli.dsl import (
    SizeContextParams,
    StimulusFamily,
    StimulusSpec,
    TaskSpec,
    TaskType,
)
from mirageforge.stimuli.renderer import StimulusRenderer


class TestStimulusRenderer:
    """Tests for StimulusRenderer."""
    
    def test_render_size_context(self):
        """Test rendering size context stimulus."""
        renderer = StimulusRenderer(image_size=512)
        
        params = SizeContextParams(
            target_size=50.0,
            context_size=80.0,
            context_distance=150.0,
            num_context=6,
            context_color="#808080",
            target_color="#000000",
            background_color="#FFFFFF",
        )
        
        task = TaskSpec(
            task_type=TaskType.TWO_AFC,
            options=["Left", "Right"],
            question="Which is larger?",
        )
        
        spec = StimulusSpec(
            family=StimulusFamily.SIZE_CONTEXT,
            params=params,
            task=task,
            seed=42,
        )
        
        image = renderer.render(spec)
        
        assert isinstance(image, Image.Image)
        assert image.size == (512, 512)
        assert image.mode == "RGB"
    
    def test_render_deterministic(self):
        """Test that rendering is deterministic."""
        renderer = StimulusRenderer(image_size=256)
        
        params = SizeContextParams(
            target_size=50.0,
            context_size=80.0,
            context_distance=150.0,
            num_context=6,
        )
        
        task = TaskSpec(
            task_type=TaskType.TWO_AFC,
            options=["A", "B"],
            question="Test?",
        )
        
        spec = StimulusSpec(
            family=StimulusFamily.SIZE_CONTEXT,
            params=params,
            task=task,
            seed=123,
        )
        
        # Render twice
        image1 = renderer.render(spec)
        image2 = renderer.render(spec)
        
        # Convert to bytes and compare
        import io
        buf1 = io.BytesIO()
        buf2 = io.BytesIO()
        image1.save(buf1, format="PNG")
        image2.save(buf2, format="PNG")
        
        assert buf1.getvalue() == buf2.getvalue()
    
    def test_render_to_file(self):
        """Test rendering to file."""
        renderer = StimulusRenderer(image_size=256)
        
        params = SizeContextParams(
            target_size=50.0,
            context_size=80.0,
            context_distance=150.0,
            num_context=6,
        )
        
        task = TaskSpec(
            task_type=TaskType.TWO_AFC,
            options=["A", "B"],
            question="Test?",
        )
        
        spec = StimulusSpec(
            family=StimulusFamily.SIZE_CONTEXT,
            params=params,
            task=task,
            seed=42,
        )
        
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "test.png"
            checksum = renderer.render_to_file(spec, output_path)
            
            assert output_path.exists()
            assert len(checksum) == 64  # SHA256 hex length
            
            # Verify image
            image = Image.open(output_path)
            assert image.size == (256, 256)
    
    def test_render_to_bytes(self):
        """Test rendering to bytes."""
        renderer = StimulusRenderer(image_size=256)
        
        params = SizeContextParams(
            target_size=50.0,
            context_size=80.0,
            context_distance=150.0,
            num_context=6,
        )
        
        task = TaskSpec(
            task_type=TaskType.TWO_AFC,
            options=["A", "B"],
            question="Test?",
        )
        
        spec = StimulusSpec(
            family=StimulusFamily.SIZE_CONTEXT,
            params=params,
            task=task,
            seed=42,
        )
        
        png_bytes, checksum = renderer.render_to_bytes(spec)
        
        assert isinstance(png_bytes, bytes)
        assert len(png_bytes) > 0
        assert len(checksum) == 64
        
        # Verify PNG signature
        assert png_bytes[:8] == b'\x89PNG\r\n\x1a\n'
