FROM texlive/texlive:latest-full AS builder

WORKDIR /app

COPY . .

RUN pdflatex -output-directory=/app/ -output-format=pdf -jobname=main /app/main.tex