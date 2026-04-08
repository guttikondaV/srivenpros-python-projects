import pytest
from unittest.mock import MagicMock, patch

from youtube_downloader import (
    get_formats,
    download_video,
    select_best_format,
    list_formats,
    parse_args,
    main,
)

SAMPLE_FORMATS = [
    {"format_id": "137", "ext": "mp4", "format_note": "1080", "height": 1080},
    {"format_id": "136", "ext": "mp4", "format_note": "720", "height": 720},
    {"format_id": "140", "ext": "m4a", "format_note": "tiny", "height": None},
]

TEST_URL = "https://www.youtube.com/watch?v=test123"


class TestGetFormats:
    @patch("youtube_downloader.yt_dlp.YoutubeDL")
    def test_returns_formats_list(self, mock_ydl_class):
        mock_ydl = MagicMock()
        mock_ydl_class.return_value.__enter__.return_value = mock_ydl
        mock_ydl.extract_info.return_value = {"formats": SAMPLE_FORMATS}

        result = get_formats(TEST_URL)

        assert result == SAMPLE_FORMATS
        mock_ydl.extract_info.assert_called_once_with(TEST_URL, download=False)

    @patch("youtube_downloader.yt_dlp.YoutubeDL")
    def test_returns_empty_list_when_no_formats(self, mock_ydl_class):
        mock_ydl = MagicMock()
        mock_ydl_class.return_value.__enter__.return_value = mock_ydl
        mock_ydl.extract_info.return_value = {}

        result = get_formats(TEST_URL)

        assert result == []


class TestDownloadVideo:
    @patch("youtube_downloader.yt_dlp.YoutubeDL")
    def test_downloads_with_format_id(self, mock_ydl_class):
        mock_ydl = MagicMock()
        mock_ydl_class.return_value.__enter__.return_value = mock_ydl

        download_video(TEST_URL, "137")

        opts = mock_ydl_class.call_args[0][0]
        assert opts["format"] == "137"
        assert opts["outtmpl"] == "%(title)s.%(ext)s"
        mock_ydl.download.assert_called_once_with([TEST_URL])

    @patch("youtube_downloader.yt_dlp.YoutubeDL")
    def test_uses_custom_output_template(self, mock_ydl_class):
        mock_ydl = MagicMock()
        mock_ydl_class.return_value.__enter__.return_value = mock_ydl

        download_video(TEST_URL, "137", output_template="/downloads/%(title)s.%(ext)s")

        opts = mock_ydl_class.call_args[0][0]
        assert opts["outtmpl"] == "/downloads/%(title)s.%(ext)s"


class TestSelectBestFormat:
    def test_selects_highest_resolution(self):
        result = select_best_format(SAMPLE_FORMATS)
        assert result == "137"  # 1080p is the highest

    def test_handles_none_height(self):
        formats = [
            {"format_id": "140", "ext": "m4a", "height": None},
            {"format_id": "136", "ext": "mp4", "height": 720},
        ]
        result = select_best_format(formats)
        assert result == "136"

    def test_single_format(self):
        formats = [{"format_id": "18", "ext": "mp4", "height": 360}]
        result = select_best_format(formats)
        assert result == "18"


class TestListFormats:
    def test_prints_all_format_ids(self, capsys):
        list_formats(SAMPLE_FORMATS)
        captured = capsys.readouterr()
        assert "137" in captured.out
        assert "136" in captured.out
        assert "140" in captured.out

    def test_prints_extensions(self, capsys):
        list_formats(SAMPLE_FORMATS)
        captured = capsys.readouterr()
        assert "mp4" in captured.out
        assert "m4a" in captured.out

    def test_prints_format_note(self, capsys):
        list_formats(SAMPLE_FORMATS)
        captured = capsys.readouterr()
        assert "1080" in captured.out
        assert "720" in captured.out

    def test_missing_format_note_shows_na(self, capsys):
        list_formats([{"format_id": "18", "ext": "mp4", "height": 360}])
        captured = capsys.readouterr()
        assert "N/A" in captured.out


class TestParseArgs:
    def test_url_is_required(self):
        with pytest.raises(SystemExit):
            parse_args([])

    def test_url_parsed(self):
        args = parse_args([TEST_URL])
        assert args.url == TEST_URL

    def test_format_short_flag(self):
        args = parse_args([TEST_URL, "-f", "137"])
        assert args.format_id == "137"

    def test_format_long_flag(self):
        args = parse_args([TEST_URL, "--format", "137"])
        assert args.format_id == "137"

    def test_best_short_flag(self):
        args = parse_args([TEST_URL, "-b"])
        assert args.best is True

    def test_best_long_flag(self):
        args = parse_args([TEST_URL, "--best"])
        assert args.best is True

    def test_list_formats_short_flag(self):
        args = parse_args([TEST_URL, "-l"])
        assert args.list_formats is True

    def test_list_formats_long_flag(self):
        args = parse_args([TEST_URL, "--list-formats"])
        assert args.list_formats is True

    def test_output_short_flag(self):
        args = parse_args([TEST_URL, "-o", "/tmp/%(title)s.%(ext)s"])
        assert args.output == "/tmp/%(title)s.%(ext)s"

    def test_output_long_flag(self):
        args = parse_args([TEST_URL, "--output", "/tmp/%(title)s.%(ext)s"])
        assert args.output == "/tmp/%(title)s.%(ext)s"

    def test_default_output(self):
        args = parse_args([TEST_URL])
        assert args.output == "%(title)s.%(ext)s"

    def test_defaults(self):
        args = parse_args([TEST_URL])
        assert args.format_id is None
        assert args.best is False
        assert args.list_formats is False


class TestMain:
    @patch("youtube_downloader.download_video")
    @patch("youtube_downloader.get_formats")
    def test_list_formats_does_not_download(self, mock_get_formats, mock_download):
        mock_get_formats.return_value = SAMPLE_FORMATS

        main([TEST_URL, "--list-formats"])

        mock_download.assert_not_called()

    @patch("youtube_downloader.download_video")
    @patch("youtube_downloader.get_formats")
    def test_downloads_with_specified_format(self, mock_get_formats, mock_download):
        mock_get_formats.return_value = SAMPLE_FORMATS

        main([TEST_URL, "-f", "137"])

        mock_download.assert_called_once_with(TEST_URL, "137", "%(title)s.%(ext)s")

    @patch("youtube_downloader.download_video")
    @patch("youtube_downloader.get_formats")
    def test_downloads_best_format(self, mock_get_formats, mock_download):
        mock_get_formats.return_value = SAMPLE_FORMATS

        main([TEST_URL, "--best"])

        mock_download.assert_called_once_with(TEST_URL, "137", "%(title)s.%(ext)s")

    @patch("youtube_downloader.download_video")
    @patch("youtube_downloader.get_formats")
    def test_uses_custom_output_with_format(self, mock_get_formats, mock_download):
        mock_get_formats.return_value = SAMPLE_FORMATS

        main([TEST_URL, "-f", "137", "-o", "/tmp/%(title)s.%(ext)s"])

        mock_download.assert_called_once_with(TEST_URL, "137", "/tmp/%(title)s.%(ext)s")

    @patch("youtube_downloader.download_video")
    @patch("youtube_downloader.get_formats")
    @patch("builtins.input", return_value="136")
    def test_interactive_format_selection(self, mock_input, mock_get_formats, mock_download):
        mock_get_formats.return_value = SAMPLE_FORMATS

        main([TEST_URL])

        mock_download.assert_called_once_with(TEST_URL, "136", "%(title)s.%(ext)s")

    @patch("youtube_downloader.download_video")
    @patch("youtube_downloader.get_formats")
    @patch("builtins.input", return_value="")
    def test_interactive_empty_input_uses_best(self, mock_input, mock_get_formats, mock_download):
        mock_get_formats.return_value = SAMPLE_FORMATS

        main([TEST_URL])

        mock_download.assert_called_once_with(TEST_URL, "137", "%(title)s.%(ext)s")
