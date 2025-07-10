# Use the official Python image
FROM python:3.12
LABEL maintainer="dc.ramzservat.com"

# Set the working directory
WORKDIR /xtrader

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV PATH="/opt/conda/bin:/scripts:/py/bin:$PATH"

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    python3-dev \
    libffi-dev \
    libssl-dev \
    libxml2 \
    libxml2-dev \
    libxslt1-dev \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    postgresql-client \
    wget \
    vim \
    redis-tools  \
    graphviz \
    less && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Miniconda
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh && \
    bash miniconda.sh -b -p /opt/conda && \
    rm miniconda.sh

# Configure Conda
RUN conda init bash && \
    conda config --set auto_activate_base false

# Create Conda environment
RUN conda create -n xtrader-env -c conda-forge python=3.12 ta-lib uwsgi && \
    conda clean -afy

# Copy requirements and install
COPY ./requirements.txt /xtrader/
RUN conda run -n xtrader-env pip install --upgrade pip && \
    conda run -n xtrader-env pip install -r /xtrader/requirements.txt

# Copy project files
COPY ./xtrader /xtrader/
COPY ./scripts /scripts

# Set up non-root user and permissions
RUN adduser --disabled-password --no-create-home xtrader && \
    mkdir -p /vol/web/static /vol/web/media && \
    chown -R xtrader:xtrader /xtrader /vol && \
    chmod -R 755 /vol && \
    chmod -R +x /scripts

# Create migration files directory for 3rd part libraries. Make xtrader user, have access to modify it. 
RUN mkdir -p /xtrader/migrations/userena && \
    mkdir -p /xtrader/migrations/guardian && \
    mkdir -p /xtrader/migrations/easy_thumbnails && \
    touch /xtrader/migrations/__init__.py && \
    touch /xtrader/migrations/userena/__init__.py && \
    touch /xtrader/migrations/guardian/__init__.py && \
    touch /xtrader/migrations/easy_thumbnails/__init__.py && \
    chown -R xtrader:xtrader /xtrader/migrations

# Switch to non-root user
USER xtrader

# Expose port
EXPOSE 9000

# Specify the default command (modified for Conda)
CMD ["conda", "run", "-n", "xtrader-env", "python", "manage.py", "runserver", "0.0.0.0:8000"]