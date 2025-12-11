FROM python:3.14-slim

WORKDIR /app

# Copy requirements first for better Docker layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the source code
COPY src/ ./src/

# Set Python path so imports work correctly
ENV PYTHONPATH=/app

# Make scanner_cli.py executable
RUN chmod +x src/scanner_cli.py

# Default command shows help
ENTRYPOINT ["python", "src/scanner_cli.py"]
CMD ["--help"]

