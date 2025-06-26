import shiva.shiva_cli


def test_cli_main(monkeypatch):
    called = {}

    def fake_command():
        called["yes"] = True

    monkeypatch.setattr(shiva.shiva_cli.ch, "command", fake_command)
    shiva.shiva_cli.main()
    assert called["yes"]
