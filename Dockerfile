FROM python:3.11-slim-bullseye

# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    # Ensure UTF-8 for gettext/django
    LANG=C.UTF-8 \
    LC_ALL=C.UTF-8

# Install system dependencies
# - curl, gnupg2: for Node.js setup
# - git: for pip git requirements
# - gettext: for django translations
# - build-essential, libpq-dev, pkg-config: for building python extensions (psycopg2, cffi)
RUN apt-get update && apt-get install -y \
    curl \
    gnupg2 \
    git \
    gettext \
    build-essential \
    libpq-dev \
    pkg-config \
    libffi-dev \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js 16
# Using nodesource setup for 16.x
RUN curl -fsSL https://deb.nodesource.com/setup_16.x | bash - && \
    apt-get install -y nodejs && \
    npm install -g yarn

WORKDIR /app

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Install Node dependencies
COPY package.json yarn.lock /app/
RUN yarn install --frozen-lockfile

# Copy project files
# Copy project files
COPY . /app/

# Initialize submodules
# We need to explicitly initialize submodules because .git might be in .dockerignore or not copied correctly otherwise.
# However, standard COPY . /app/ copies the .git directory if it is not ignored.
# We must ensure .git is NOT ignored for this step to work, OR we must clone the submodule explicitly.
# Since we are inside the build, and the context is sent to the daemon, we rely on the context having the .git folder if we want to use git commands.
# BUT: It is best practice to NOT copy .git into the image for size reasons.
# A better approach for Dokku (which builds from git) is to rely on the fact that Dokku might not send the .git folder in the context if using `git push`.
# If the user pushes via `git push dokku`, Dokku checks out the code.
# The user says "we have to run git submodule init".
# If I remove .git from .dockerignore, the entire history is copied.
# Let's try running the command the user asked for.
RUN git submodule update --init --recursive

# Build checks:
# 1. Build frontend (React Check-in)
RUN yarn build

# 2. Collect static files (replicating predeploy.sh exclusions)
# We set a dummy SECRET_KEY to ensure collectstatic runs without needing the real prod secret
RUN SECRET_KEY=build_dummy python manage.py collectstatic -i node_modules -i src -i package.json -i public -i scripts -i *.lock --noinput

# 3. Compile translations
RUN django-admin compilemessages

# Cleanup
RUN rm -rf node_modules

# Runtime command
# Uses port 8000 by default, ensure your host maps to this
EXPOSE 8000

CMD ["gunicorn", "jararaca.wsgi", "--bind", "0.0.0.0:8000", "--timeout", "600", "--access-logfile", "-", "--error-logfile", "-"]
