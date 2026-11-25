"""Telegram API 示例（Telegram API in Python）。

  python main.py channel durov                     # 频道资料 / channel profile
  python main.py posts durov --out posts.csv       # 频道帖子 / channel posts
  python main.py search bitcoin --out messages.csv # 搜公开消息 / search messages
"""
import argparse

from everyinfra import fetch, report


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("channel", help="频道资料 / channel profile")
    c.add_argument("username")
    po = sub.add_parser("posts", help="频道帖子 / a channel's posts")
    po.add_argument("username")
    s = sub.add_parser("search", help="按关键词搜公开消息 / search public messages")
    s.add_argument("keyword")
    s.add_argument("--since", help="起始日期 YYYY-MM-DD / start date")
    s.add_argument("--until", help="截止日期 YYYY-MM-DD / end date")
    for x in (c, po, s):
        x.add_argument("--out", help="存成 .csv 或 .json / write .csv or .json")
    a = p.parse_args()

    if a.cmd == "channel":
        rows, charged = fetch("profile", {"username": a.username})
    elif a.cmd == "posts":
        rows, charged = fetch("channel_posts", {"username": a.username})
    else:
        params = {"keyword": a.keyword, **({"since": a.since} if a.since else {}), **({"until": a.until} if a.until else {})}
        rows, charged = fetch("search", params)
    report(rows, charged, a.out)


if __name__ == "__main__":
    main()
