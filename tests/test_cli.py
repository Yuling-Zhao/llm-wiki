from llm_wiki.cli import main


def run_cli(*args: str) -> int:
    return main(list(args))


def test_cli_help_returns_success(capsys):
    exit_code = run_cli("--help")

    assert exit_code == 0
    assert "llm-wiki" in capsys.readouterr().out


def test_init_creates_workspace(tmp_path):
    target = tmp_path / "my-wiki"

    exit_code = run_cli("init", str(target))

    assert exit_code == 0
    assert (target / "AGENTS.md").is_file()
    assert (target / "raw").is_dir()
    assert (target / "wiki" / "index.md").is_file()
    assert (target / "wiki" / "log.md").is_file()
    assert (target / "wiki" / "overview.md").is_file()


def test_init_includes_pdf_ingest_workflow(tmp_path):
    target = tmp_path / "my-wiki"

    exit_code = run_cli("init", str(target))

    agents_text = (target / "AGENTS.md").read_text(encoding="utf-8")
    assert exit_code == 0
    assert "command -v pdftotext" in agents_text
    assert "pdftotext -layout" in agents_text
    assert "/tmp/trim-pdf-text/<source-title>.txt" in agents_text
    assert "keep the original PDF as the source reference" in agents_text


def test_init_refuses_non_empty_directory(tmp_path, capsys):
    target = tmp_path / "existing"
    target.mkdir()
    (target / "note.txt").write_text("keep me", encoding="utf-8")

    exit_code = run_cli("init", str(target))

    assert exit_code == 1
    assert "refusing to initialize non-empty directory" in capsys.readouterr().err
    assert (target / "note.txt").read_text(encoding="utf-8") == "keep me"


def test_doctor_succeeds_for_fresh_workspace(tmp_path, capsys):
    target = tmp_path / "my-wiki"
    assert run_cli("init", str(target)) == 0

    exit_code = run_cli("doctor", str(target))

    assert exit_code == 0
    assert "workspace ok" in capsys.readouterr().out


def test_doctor_fails_when_required_file_missing(tmp_path, capsys):
    target = tmp_path / "my-wiki"
    assert run_cli("init", str(target)) == 0
    (target / "wiki" / "index.md").unlink()

    exit_code = run_cli("doctor", str(target))

    assert exit_code == 1
    assert "missing: wiki/index.md" in capsys.readouterr().err


def test_doctor_warns_when_pdfs_need_pdftotext(tmp_path, capsys, monkeypatch):
    target = tmp_path / "my-wiki"
    assert run_cli("init", str(target)) == 0
    (target / "raw" / "paper.pdf").write_bytes(b"%PDF-1.4\n")
    monkeypatch.setattr("llm_wiki.cli.shutil.which", lambda name: None)

    exit_code = run_cli("doctor", str(target))

    captured = capsys.readouterr()
    assert exit_code == 0
    assert "workspace ok" in captured.out
    assert "warning: raw/ contains PDF files but pdftotext was not found" in captured.err
    assert "brew install poppler" in captured.err
    assert "outside raw/ with pdftotext -layout" in captured.err


def test_log_prints_recent_entries(tmp_path, capsys):
    target = tmp_path / "my-wiki"
    assert run_cli("init", str(target)) == 0
    (target / "wiki" / "log.md").write_text(
        "\n".join(
            [
                "# Wiki Log",
                "",
                "## [2026-04-18] ingest | First Source",
                "",
                "## [2026-04-19] query | Comparison",
                "",
                "## [2026-04-20] lint | Weekly check",
                "",
            ]
        ),
        encoding="utf-8",
    )

    exit_code = run_cli("log", str(target), "--limit", "2")

    assert exit_code == 0
    assert capsys.readouterr().out.splitlines() == [
        "2026-04-19 query | Comparison",
        "2026-04-20 lint | Weekly check",
    ]


def test_index_prints_links_and_summaries(tmp_path, capsys):
    target = tmp_path / "my-wiki"
    assert run_cli("init", str(target)) == 0
    (target / "wiki" / "index.md").write_text(
        "\n".join(
            [
                "# Wiki Index",
                "",
                "- [Overview](overview.md) - Current synthesis.",
                "- [Entity A](entities/entity-a.md) - Important entity.",
            ]
        ),
        encoding="utf-8",
    )

    exit_code = run_cli("index", str(target))

    assert exit_code == 0
    assert capsys.readouterr().out.splitlines() == [
        "Overview | overview.md | Current synthesis.",
        "Entity A | entities/entity-a.md | Important entity.",
    ]
