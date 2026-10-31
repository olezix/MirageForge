"""
FastAPI web application for MirageForge.

Provides web interface for experiments, dashboard, and API endpoints.
"""

from datetime import datetime
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from mirageforge import __version__
from mirageforge.config import get_settings
from mirageforge.db import get_db_global, get_engine, init_db
from mirageforge.schemas import (
    ExperimentConfig,
    HealthResponse,
    ResponseCreate,
    SessionCreate,
)

# Initialize FastAPI app
app = FastAPI(
    title="MirageForge",
    description="Visual illusion research platform",
    version=__version__,
    docs_url="/docs" if get_settings().debug else None,
    redoc_url="/redoc" if get_settings().debug else None,
)


# Security headers middleware
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    # CSP - Content Security Policy
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data:;"
    )
    return response


# CORS middleware (for development)
if get_settings().is_development():
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Templates
templates_dir = Path(__file__).parent / "templates"
templates_dir.mkdir(exist_ok=True)
templates = Jinja2Templates(directory=str(templates_dir))

# Static files
static_dir = Path(__file__).parent / "static"
static_dir.mkdir(exist_ok=True)
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup."""
    engine = get_engine()
    init_db(engine)


@app.get("/", response_class=HTMLResponse)
async def landing_page(request: Request):
    """Landing page with information about the platform."""
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>MirageForge - Visual Illusion Research Platform</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; line-height: 1.6; }
            h1 { color: #333; }
            .warning { background: #fff3cd; border: 2px solid #ffc107; padding: 15px; margin: 20px 0; border-radius: 5px; }
            .button { display: inline-block; padding: 12px 24px; background: #007bff; color: white; text-decoration: none; border-radius: 5px; margin: 10px 5px; }
            .button:hover { background: #0056b3; }
            .disclaimer { background: #f8f9fa; padding: 15px; border-left: 4px solid #6c757d; margin: 20px 0; }
        </style>
    </head>
    <body>
        <h1>MirageForge</h1>
        <p><strong>Open research platform for AI-driven discovery of candidate visual illusions</strong></p>

        <div class="warning">
            <strong>⚠️ Research Platform</strong><br>
            This is a research platform for studying visual perception.
            It is not a medical or diagnostic tool.
            Participation is voluntary and anonymous.
        </div>

        <h2>About</h2>
        <p>MirageForge uses AI to generate candidate visual stimuli and compares human perception
        with vision model predictions to identify interesting perceptual phenomena.</p>

        <h2>Participate in an Experiment</h2>
        <p>If you are 18 or older and interested in participating in a visual perception experiment:</p>
        <a href="/consent" class="button">Start Experiment</a>

        <h2>Explore</h2>
        <p><a href="/gallery" class="button">View Gallery</a>
        <a href="/dashboard" class="button">View Dashboard</a></p>

        <div class="disclaimer">
            <strong>Disclaimer:</strong> This platform is for research purposes only.
            It does not provide medical diagnoses or treatment.
            If you have concerns about your vision, please consult a healthcare professional.
        </div>

        <footer style="margin-top: 40px; padding-top: 20px; border-top: 1px solid #ddd; color: #666; font-size: 14px;">
            <p>MirageForge v1.0.0 | <a href="/healthz">Health Check</a> | <a href="/docs">API Documentation</a></p>
        </footer>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)


@app.get("/consent", response_class=HTMLResponse)
async def consent_page(request: Request):
    """Consent form page."""
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Consent - MirageForge</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 700px; margin: 50px auto; padding: 20px; line-height: 1.6; }
            .consent-box { background: #f8f9fa; padding: 20px; border-radius: 5px; margin: 20px 0; }
            .checkbox-group { margin: 20px 0; }
            .checkbox-group label { display: block; margin: 10px 0; }
            .button { display: inline-block; padding: 12px 24px; background: #007bff; color: white; text-decoration: none; border-radius: 5px; border: none; cursor: pointer; font-size: 16px; }
            .button:hover { background: #0056b3; }
            .button:disabled { background: #ccc; cursor: not-allowed; }
        </style>
    </head>
    <body>
        <h1>Informed Consent</h1>

        <div class="consent-box">
            <h2>About This Experiment</h2>
            <p>You are invited to participate in a visual perception experiment.
            During this experiment, you will view various visual patterns and answer questions
            about what you see.</p>

            <h3>What to Expect</h3>
            <ul>
                <li>The experiment takes approximately 5-10 minutes</li>
                <li>You will view static visual patterns on your screen</li>
                <li>You will answer questions about your perception</li>
                <li>Your responses will be recorded anonymously</li>
            </ul>

            <h3>Your Rights</h3>
            <ul>
                <li>Participation is completely voluntary</li>
                <li>You may stop at any time without penalty</li>
                <li>Your data is anonymous - we do not collect personal information</li>
                <li>You must be 18 or older to participate</li>
            </ul>

            <h3>Risks</h3>
            <p>Some visual patterns may cause mild visual discomfort.
            If you experience any discomfort, please stop immediately and look away from the screen.</p>

            <h3>Important</h3>
            <p><strong>This is NOT a medical test.</strong> It does not diagnose any conditions.
            If you have concerns about your vision, please consult a healthcare professional.</p>
        </div>

        <form id="consentForm" action="/api/session" method="post">
            <div class="checkbox-group">
                <label>
                    <input type="checkbox" id="age18" required>
                    I confirm that I am 18 years of age or older
                </label>
                <label>
                    <input type="checkbox" id="understand" required>
                    I understand the information provided above
                </label>
                <label>
                    <input type="checkbox" id="voluntary" required>
                    I understand that participation is voluntary and I may stop at any time
                </label>
                <label>
                    <input type="checkbox" id="consent" required>
                    I consent to participate in this experiment
                </label>
            </div>

            <button type="submit" class="button" id="startButton" disabled>Start Experiment</button>
            <a href="/" class="button" style="background: #6c757d;">Cancel</a>
        </form>

        <script>
            const checkboxes = document.querySelectorAll('input[type="checkbox"]');
            const startButton = document.getElementById('startButton');

            function checkAllChecked() {
                const allChecked = Array.from(checkboxes).every(cb => cb.checked);
                startButton.disabled = !allChecked;
            }

            checkboxes.forEach(cb => cb.addEventListener('change', checkAllChecked));

            document.getElementById('consentForm').addEventListener('submit', async function(e) {
                e.preventDefault();

                const response = await fetch('/api/session', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({study_id: 1, consent_version: '1.0.0'})
                });

                if (response.ok) {
                    const data = await response.json();
                    window.location.href = `/experiment?session=${data.id}`;
                } else {
                    alert('Failed to start session. Please try again.');
                }
            });
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)


@app.get("/experiment", response_class=HTMLResponse)
async def experiment_page(request: Request, session: str):
    """Experiment page with trials."""
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Experiment - MirageForge</title>
        <style>
            body {{ font-family: Arial, sans-serif; max-width: 900px; margin: 20px auto; padding: 20px; }}
            .progress {{ background: #e9ecef; height: 20px; border-radius: 10px; margin: 20px 0; }}
            .progress-bar {{ background: #007bff; height: 100%; border-radius: 10px; transition: width 0.3s; }}
            .stimulus {{ text-align: center; margin: 30px 0; }}
            .stimulus img {{ max-width: 512px; height: auto; border: 2px solid #ddd; }}
            .question {{ font-size: 18px; margin: 20px 0; text-align: center; }}
            .options {{ display: flex; flex-direction: column; gap: 10px; max-width: 500px; margin: 20px auto; }}
            .option-button {{ padding: 15px; background: #007bff; color: white; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; }}
            .option-button:hover {{ background: #0056b3; }}
            .stop-button {{ background: #dc3545; margin-top: 30px; }}
            .stop-button:hover {{ background: #c82333; }}
        </style>
    </head>
    <body>
        <h1>Visual Perception Experiment</h1>
        <div class="progress">
            <div class="progress-bar" id="progressBar" style="width: 0%"></div>
        </div>
        <p id="progressText">Trial 0 of 12</p>

        <div id="trialContainer">
            <div class="stimulus">
                <img id="stimulusImage" src="" alt="Visual stimulus">
            </div>
            <div class="question" id="questionText"></div>
            <div class="options" id="optionsContainer"></div>
        </div>

        <button class="option-button stop-button" onclick="stopExperiment()">Stop Experiment</button>

        <script>
            const sessionId = '{session}';
            let currentTrial = null;
            let trialCount = 0;
            const totalTrials = 12;
            let trialStartTime = null;

            async function loadNextTrial() {{
                const response = await fetch('/api/trial', {{
                    method: 'POST',
                    headers: {{'Content-Type': 'application/json'}},
                    body: JSON.stringify({{session_id: sessionId}})
                }});

                if (!response.ok) {{
                    window.location.href = '/debrief?session=' + sessionId;
                    return;
                }}

                currentTrial = await response.json();
                trialCount++;

                // Update progress
                const progress = (trialCount / totalTrials) * 100;
                document.getElementById('progressBar').style.width = progress + '%';
                document.getElementById('progressText').textContent = `Trial ${{trialCount}} of ${{totalTrials}}`;

                // Display trial
                document.getElementById('stimulusImage').src = '/static/stimuli/' + currentTrial.stimulus.image_path.split('/').pop();
                document.getElementById('questionText').textContent = currentTrial.stimulus.task_spec.question;

                const optionsContainer = document.getElementById('optionsContainer');
                optionsContainer.innerHTML = '';

                const options = Object.keys(currentTrial.option_order);
                options.forEach(option => {{
                    const button = document.createElement('button');
                    button.className = 'option-button';
                    button.textContent = option;
                    button.onclick = () => submitResponse(option);
                    optionsContainer.appendChild(button);
                }});

                trialStartTime = Date.now();
            }}

            async function submitResponse(choice) {{
                const reactionTime = Date.now() - trialStartTime;

                await fetch('/api/response', {{
                    method: 'POST',
                    headers: {{'Content-Type': 'application/json'}},
                    body: JSON.stringify({{
                        trial_id: currentTrial.id,
                        choice: choice,
                        reaction_time_ms: reactionTime
                    }})
                }});

                if (trialCount >= totalTrials) {{
                    await fetch('/api/complete', {{
                        method: 'POST',
                        headers: {{'Content-Type': 'application/json'}},
                        body: JSON.stringify({{session_id: sessionId}})
                    }});
                    window.location.href = '/debrief?session=' + sessionId;
                }} else {{
                    loadNextTrial();
                }}
            }}

            async function stopExperiment() {{
                if (confirm('Are you sure you want to stop the experiment?')) {{
                    window.location.href = '/debrief?session=' + sessionId;
                }}
            }}

            // Start first trial
            loadNextTrial();
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)


@app.get("/debrief", response_class=HTMLResponse)
async def debrief_page(request: Request, session: str | None = None):
    """Debrief page after experiment."""
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Thank You - MirageForge</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 700px; margin: 50px auto; padding: 20px; line-height: 1.6; }
            .success { background: #d4edda; border: 2px solid #28a745; padding: 20px; border-radius: 5px; margin: 20px 0; }
            .info { background: #d1ecf1; border-left: 4px solid #17a2b8; padding: 15px; margin: 20px 0; }
        </style>
    </head>
    <body>
        <h1>Thank You!</h1>

        <div class="success">
            <h2>Experiment Complete</h2>
            <p>Thank you for participating in this visual perception experiment.
            Your anonymous responses have been recorded.</p>
        </div>

        <h2>What Was This About?</h2>
        <p>This experiment studied visual perception using various visual patterns.
        The goal is to understand how humans perceive visual stimuli and to compare
        human perception with computer vision models.</p>

        <div class="info">
            <h3>Important Notes</h3>
            <ul>
                <li><strong>This is NOT a medical test.</strong> It does not diagnose any conditions.</li>
                <li>Your data is completely anonymous - we cannot identify you.</li>
                <li>Results from this experiment contribute to research on visual perception.</li>
            </ul>
        </div>

        <h2>Learn More</h2>
        <p><a href="/gallery">View the gallery</a> to see candidate stimuli from our research.</p>
        <p><a href="/dashboard">View the dashboard</a> to see aggregate statistics.</p>

        <p><a href="/">Return to home page</a></p>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)


@app.get("/gallery", response_class=HTMLResponse)
async def gallery_page(request: Request):
    """Gallery of candidate stimuli."""
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Gallery - MirageForge</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            .warning { background: #fff3cd; border: 2px solid #ffc107; padding: 15px; margin: 20px 0; border-radius: 5px; }
        </style>
    </head>
    <body>
        <h1>Stimulus Gallery</h1>
        <div class="warning">
            <strong>Note:</strong> Gallery will be populated after running the demo pipeline.
            Run: <code>python -m mirageforge.cli demo --out artifacts/demo --seed 42</code>
        </div>
        <p><a href="/">Return to home</a></p>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)


@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard_page(request: Request):
    """Dashboard with aggregate statistics."""
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Dashboard - MirageForge</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            .stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin: 20px 0; }
            .stat-card { background: #f8f9fa; padding: 20px; border-radius: 5px; text-align: center; }
            .stat-value { font-size: 36px; font-weight: bold; color: #007bff; }
            .stat-label { color: #666; margin-top: 10px; }
        </style>
    </head>
    <body>
        <h1>Dashboard</h1>
        <p>Aggregate statistics from experiments (anonymous data only).</p>

        <div class="stats">
            <div class="stat-card">
                <div class="stat-value">-</div>
                <div class="stat-label">Total Sessions</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">-</div>
                <div class="stat-label">Completed</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">-</div>
                <div class="stat-label">Total Responses</div>
            </div>
        </div>

        <p><em>Statistics will appear after experiments are conducted.</em></p>
        <p><a href="/">Return to home</a></p>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)


@app.get("/healthz", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="ok",
        version=__version__,
        timestamp=datetime.utcnow(),
    )


# API Endpoints


@app.post("/api/session")
async def create_session(session_data: SessionCreate):
    """Create a new experiment session."""
    from mirageforge.experiment.service import ExperimentService

    with get_db_global() as db:
        service = ExperimentService(db)
        session = service.create_session(session_data)
        return {"id": session.id, "status": session.status}


@app.post("/api/trial")
async def get_next_trial(request: Request):
    """Get next trial for session."""
    from mirageforge.experiment.service import ExperimentService

    data = await request.json()
    session_id = data.get("session_id")

    if not session_id:
        raise HTTPException(status_code=400, detail="session_id required")

    with get_db_global() as db:
        service = ExperimentService(db)
        config = ExperimentConfig(study_id=1, trials_count=12)
        trial = service.get_next_trial(session_id, config)

        if trial is None:
            raise HTTPException(status_code=404, detail="No more trials")

        return trial.model_dump()


@app.post("/api/response")
async def record_response(response_data: ResponseCreate):
    """Record a response to a trial."""
    from mirageforge.experiment.service import ExperimentService

    with get_db_global() as db:
        service = ExperimentService(db)
        service.record_response(response_data)
        return {"status": "ok"}


@app.post("/api/complete")
async def complete_session(request: Request):
    """Complete a session."""
    from mirageforge.experiment.service import ExperimentService

    data = await request.json()
    session_id = data.get("session_id")

    if not session_id:
        raise HTTPException(status_code=400, detail="session_id required")

    with get_db_global() as db:
        service = ExperimentService(db)
        session = service.complete_session(session_id)
        return {"status": "completed", "id": session.id}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
