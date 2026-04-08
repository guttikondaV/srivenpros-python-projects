import argparse
import yt_dlp


def get_formats(url):
    """Extracts available formats for a YouTube video."""
    ydl_opts = {"quiet": True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        return info_dict.get("formats", [])


def download_video(url, format_id, output_template="%(title)s.%(ext)s"):
    """Downloads a YouTube video with the specified format."""
    ydl_opts = {
        "format": format_id,
        "outtmpl": output_template,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


def select_best_format(formats):
    """Returns the format ID with the highest resolution."""
    best = max(formats, key=lambda x: x.get("height") or 0)
    return best["format_id"]


def list_formats(formats):
    """Prints available formats to stdout."""
    for f in formats:
        print(f"{f['format_id']}:\t{f['ext']} ({f.get('format_note', 'N/A')})")


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        description="Download YouTube videos using yt-dlp",
        prog="youtube_downloader",
    )
    parser.add_argument("url", help="YouTube video URL")
    parser.add_argument(
        "-f", "--format",
        dest="format_id",
        help="Format ID to download (skips interactive prompt)",
    )
    parser.add_argument(
        "-b", "--best",
        action="store_true",
        help="Automatically download the best quality",
    )
    parser.add_argument(
        "-l", "--list-formats",
        action="store_true",
        help="List available formats and exit",
    )
    parser.add_argument(
        "-o", "--output",
        default="%(title)s.%(ext)s",
        help="Output filename template (default: %%(title)s.%%(ext)s)",
    )
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    formats = get_formats(args.url)

    if args.list_formats:
        list_formats(formats)
        return

    if args.format_id:
        format_id = args.format_id
    elif args.best:
        format_id = select_best_format(formats)
        print(f"Selected best format: {format_id}")
    else:
        list_formats(formats)
        format_id = input("Enter the format ID to download (or press Enter for best): ").strip()
        if not format_id:
            format_id = select_best_format(formats)
            print(f"Selected best format: {format_id}")

    download_video(args.url, format_id, args.output)
    print("Download complete!")


if __name__ == "__main__":
    main()
