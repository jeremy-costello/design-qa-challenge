FROM astral/uv:bookworm-slim

WORKDIR /working

RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

RUN git clone --depth 1 --single-branch \
    https://github.com/anniedoris/design_qa.git \
    ./vendor/design_qa

COPY ./tasks .
COPY ./utils .
COPY .python-version .
COPY evaluate.sh .
COPY pyproject.toml .
COPY uv.lock .

RUN uv python install 3.13
RUN uv venv --python 3.13
RUN uv sync --locked

RUN chmod +x evaluate.sh

CMD ["./evaluate.sh"]
