# Install System and Dependencies
FROM python:3.13

# Create working directories
RUN mkdir -p /usr/src/bot
WORKDIR /usr/src/bot

# Copy into working directories
COPY . .

# Install dependencies with pip
RUN pip3 install -r requirement.txt

# Run the bot
CMD ["python3", "main.py"]
