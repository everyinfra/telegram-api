# Telegram API

[English](#english) · [中文](#中文)

## English

This repo reads public Telegram data with Python or curl. You can look up a public channel's profile and posts, and search public channel messages by keyword. You need one EveryInfra API key. You do not need a Telegram account or cookie. The same API also works as an MCP tool in Claude and Cursor. Billing is per call: these 3 capabilities cost $0.56 per 1,000 calls (about $0.00056 per call). Failed calls and empty results are not charged. The EveryInfra Telegram API has 6 capabilities, all listed on the platform page: <https://everyinfra.com/en/telegram-api?utm_source=github&utm_medium=example_repo&utm_campaign=telegram-api>

### Quick start

```bash
git clone https://github.com/everyinfra/telegram-api.git
cd telegram-api
pip install -r requirements.txt
export EVERYINFRA_API_KEY=<your API key>
python main.py channel durov
python main.py posts durov --out posts.csv
python main.py search bitcoin --out messages.csv
```

- For `channel` and `posts`, pass a public channel's username: name, @name or t.me/name all work.
- `search` only covers public channel messages, not private chats or contacts.
- Without `--out`, the command prints the first 3 rows as JSON. With `--out`, it saves a .csv or .json file. The CSV has a BOM, so Excel opens it without garbled text.
- Register at everyinfra.com, then create the API key in the console. Steps: <https://everyinfra.com/en/docs?utm_source=github&utm_medium=example_repo&utm_campaign=telegram-api#quickstart>

### curl

```bash
curl -X POST https://api.everyinfra.com/api/v1/social \
  -H "Authorization: Bearer $EVERYINFRA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"platform":"telegram","action":"profile","params":{"username":"durov"}}'
```

All capabilities use the same URL. Change `action` and `params` to call another one. Examples for `channel_posts` and `search` are in [examples/curl.sh](examples/curl.sh).

### Claude and Cursor (MCP)

The remote MCP URL is <https://api.everyinfra.com/mcp>. Add the `Authorization: Bearer` header with your API key. EveryInfra runs the server, so you install no local program.

Claude Code:

```bash
claude mcp add --transport http everyinfra https://api.everyinfra.com/mcp --header "Authorization: Bearer <API Key>"
```

Cursor and other clients that read `mcp.json` ([examples/mcp.json](examples/mcp.json)):

```json
{
  "mcpServers": {
    "everyinfra": {
      "url": "https://api.everyinfra.com/mcp",
      "headers": {
        "Authorization": "Bearer <API Key>"
      }
    }
  }
}
```

Custom connectors in Claude on the web and desktop, and ChatGPT, accept only a URL. Enter <https://api.everyinfra.com/mcp/all>, sign in to EveryInfra when asked, and allow access. You do not need to enter a key. Full steps: <https://everyinfra.com/en/mcp-server?utm_source=github&utm_medium=example_repo&utm_campaign=telegram-api>

### Price

| `action` | Per 1,000 calls |
|---|---|
| `profile` | $0.56 |
| `channel_posts` | $0.56 |
| `search` | $0.56 |

- Billing is per call, about $0.00056 each. Failed calls, empty results, parameter errors, and authentication failures are not charged.
- A new account gets a $1 trial allowance, valid for 24 hours. No credit card is needed. How to claim it: <https://everyinfra.com/en/pricing?utm_source=github&utm_medium=example_repo&utm_campaign=telegram-api>
- Prices for the other 3 Telegram capabilities are on the platform page: <https://everyinfra.com/en/telegram-api?utm_source=github&utm_medium=example_repo&utm_campaign=telegram-api>

### Fields

These are the fields that the 3 capabilities returned in our test. Each meaning is the first sentence of the field's entry in the API documentation. The link under each table has the full text.

#### `profile` (profile or object details)

| Field | Meaning |
|---|---|
| `username` | Username (@handle). |
| `name` | Name of the object itself, for account, product and business capabilities. |
| `bio` | Profile bio written by the account; may contain line breaks and emoji. |
| `subscriber_count` | Number of subscribers. |
| `photo_count` | Number of photos. |
| `video_count` | Number of videos. |
| `link_count` | Number of links in the message. |
| `is_verified` | Whether the platform verified the account. null means it cannot be determined. |
| `avatar_url` | Avatar image link. |
| `url` | Link to the record on the platform. |
| `platform` | Source platform identifier, the same as platform in the request (for example xiaohongshu, tiktok). |

All parameters and fields: <https://everyinfra.com/en/telegram-api/profile?utm_source=github&utm_medium=example_repo&utm_campaign=telegram-api>

#### `channel_posts` (channel posts)

| Field | Meaning |
|---|---|
| `id` | The record's unique ID on the platform. |
| `url` | Link to the record on the platform. |
| `channel_username` | Channel username (the public identifier starting with @). |
| `channel_title` | Channel name. |
| `text` | Body text with HTML removed, returned in full and never cut short (on a few platforms the list results themselves carry only an excerpt; the platform's field notes say so). |
| `view_count` | Views or plays. null means not disclosed, not 0. |
| `posted_at` | Publish time in ISO 8601, UTC (for example 2026-08-07T12:34:56+00:00). |
| `media_type` | Media type (photo / video / file / voice). |
| `author` | Message sender. |
| `platform` | Source platform identifier, the same as platform in the request (for example xiaohongshu, tiktok). |
| `reactions` | Emoji reactions with their counts. |
| `media_url` | Media file link. |
| `reply_to_url` | Link to the message being replied to. |
| `is_forwarded` | Whether the message is forwarded. |

All parameters and fields: <https://everyinfra.com/en/telegram-api/channel_posts?utm_source=github&utm_medium=example_repo&utm_campaign=telegram-api>

#### `search` (keyword search)

| Field | Meaning |
|---|---|
| `id` | The record's unique ID on the platform. |
| `url` | Link to the record on the platform. |
| `text` | Body text with HTML removed, returned in full and never cut short (on a few platforms the list results themselves carry only an excerpt; the platform's field notes say so). |
| `posted_at` | Publish time in ISO 8601, UTC (for example 2026-08-07T12:34:56+00:00). |
| `view_count` | Views or plays. null means not disclosed, not 0. |
| `media_url` | Media file link. |
| `channel_username` | Channel username (the public identifier starting with @). |
| `channel_title` | Channel name. |
| `channel_type` | Type (channel / group / supergroup). |
| `channel_subscriber_count` | Number of channel subscribers. |
| `channel_description` | Channel description. |
| `platform` | Source platform identifier, the same as platform in the request (for example xiaohongshu, tiktok). |

All parameters and fields: <https://everyinfra.com/en/telegram-api/search?utm_source=github&utm_medium=example_repo&utm_campaign=telegram-api>

### FAQ

**Do I need a Telegram account or cookie to call the API?**

No. Send the `Authorization: Bearer` header with your API key. The request body holds `platform`, `action`, and the capability parameters. You do not scan a QR code, keep a login session, or open a browser.

**How much does it cost? Are failed calls charged? Is there a free allowance?**

Billing is per call, from $0.56 per 1,000 calls. Failed calls, empty results, parameter errors, and authentication failures are not charged. A new account gets a $1 trial allowance, valid for 24 hours. No credit card is needed. How to claim it: <https://everyinfra.com/en/pricing?utm_source=github&utm_medium=example_repo&utm_campaign=telegram-api>

**Can I connect the Telegram API to Claude or Cursor?**

Yes. The remote MCP URL is <https://api.everyinfra.com/mcp>. Add the `Authorization: Bearer` header with your API key. You install no local program. Setup for Claude, Cursor, ChatGPT, and Claude Code: <https://everyinfra.com/en/mcp-server?utm_source=github&utm_medium=example_repo&utm_campaign=telegram-api>.

**What legal points apply when I use Telegram data?**

The EveryInfra Terms of Service require you to make sure your use of the data follows applicable law and the terms of the relevant platform. Do not use the data for anything illegal or anything that violates privacy or intellectual property rights. Do not use bulk scraping for harassment, fraud, or other abuse. When you use personal information such as nicknames and avatars, keep only the fields your business needs.

**Which Telegram data can I get?**

The EveryInfra Telegram API has 6 capabilities:

- channel posts
- profile or object details
- keyword search
- group
- members
- post details

Parameters and return fields for each capability are on the platform page: <https://everyinfra.com/en/telegram-api?utm_source=github&utm_medium=example_repo&utm_campaign=telegram-api>

### Tested

Before release, we ran the 3 commands in Quick start against the live API with this repo's code.

| Command | Time (Singapore, UTC+8) | Rows | Charged |
|---|---|---|---|
| `python main.py channel durov` | 2026-11-25 15:32 | 1 | $0.000556 |
| `python main.py posts durov --out posts.csv` | 2026-11-25 13:21 | 20 | $0.000556 |
| `python main.py search bitcoin --out messages.csv` | 2026-11-25 13:21 | 20 | $0.000556 |

## 中文

本仓库用 Python 或 curl 读 Telegram 公开数据：查公开频道资料和频道帖子，按关键词搜公开频道消息。只需一把 EveryInfra API Key，不用 Telegram 账号和 Cookie，也能作为 MCP 工具接进 Claude、Cursor。按调用次数计费，这 3 个能力每千次 $0.56（每次约 $0.00056），失败和空结果不收费。Telegram 共 6 个能力：<https://everyinfra.com/telegram-api?utm_source=github&utm_medium=example_repo&utm_campaign=telegram-api>

### 快速开始

```bash
git clone https://github.com/everyinfra/telegram-api.git
cd telegram-api
pip install -r requirements.txt
export EVERYINFRA_API_KEY=<你的 API Key>
python main.py channel durov
python main.py posts durov --out posts.csv
python main.py search bitcoin --out messages.csv
```

- `channel` 和 `posts` 传公开频道的用户名，name、@name、t.me/name 都行。
- `search` 只搜公开频道的消息，不搜私聊和联系人。
- 不加 `--out` 时打印前 3 条 JSON；加 `--out` 存成 .csv 或 .json。CSV 带 BOM，Excel 直接打开不乱码。
- API Key 在 everyinfra.com 注册后到控制台创建，步骤见 <https://everyinfra.com/docs?utm_source=github&utm_medium=example_repo&utm_campaign=telegram-api#quickstart>

### 用 curl 调

```bash
curl -X POST https://api.everyinfra.com/api/v1/social \
  -H "Authorization: Bearer $EVERYINFRA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"platform":"telegram","action":"profile","params":{"username":"durov"}}'
```

所有能力都发到同一个地址，换 `action` 和 `params` 就行；`channel_posts`、`search` 的写法见 [examples/curl.sh](examples/curl.sh)。

### 接进 Claude、Cursor（MCP）

远程 MCP 地址是 <https://api.everyinfra.com/mcp>，请求头加 `Authorization: Bearer` 和 API Key；服务器由 EveryInfra 运行，不用装本地程序。

Claude Code：

```bash
claude mcp add --transport http everyinfra https://api.everyinfra.com/mcp --header "Authorization: Bearer <API Key>"
```

Cursor 等读 `mcp.json` 的客户端（[examples/mcp.json](examples/mcp.json)）：

```json
{
  "mcpServers": {
    "everyinfra": {
      "url": "https://api.everyinfra.com/mcp",
      "headers": {
        "Authorization": "Bearer <API Key>"
      }
    }
  }
}
```

Claude 网页版和桌面版的自定义连接器、ChatGPT 只能填网址：填 <https://api.everyinfra.com/mcp/all>，连接时登录 EveryInfra 并允许，不用填 Key。完整步骤见 <https://everyinfra.com/mcp-server?utm_source=github&utm_medium=example_repo&utm_campaign=telegram-api>

### 价格

| 能力 | `action` | 每千次 |
|---|---|---|
| 主页或对象详情 | `profile` | $0.56 |
| 频道帖子 | `channel_posts` | $0.56 |
| 关键词搜索 | `search` | $0.56 |

- 按调用次数计费，每次约 $0.00056；失败、空结果、参数错误和鉴权失败都不收费。
- 新账号有 $1 试用额度，24 小时内有效，不用信用卡，领取方式见 <https://everyinfra.com/pricing?utm_source=github&utm_medium=example_repo&utm_campaign=telegram-api>
- Telegram 其他 3 个能力的单价见平台页 <https://everyinfra.com/telegram-api?utm_source=github&utm_medium=example_repo&utm_campaign=telegram-api>

### 返回字段

下面是这 3 个能力实测返回的字段，含义取自接口文档每条说明的第一句，完整说明在每张表下面的链接里。

#### `profile`（主页或对象详情）

| 字段 | 含义 |
|---|---|
| `username` | 用户名（@handle）。 |
| `name` | 名称。 |
| `bio` | 个人简介，账号自己填写的文本。 |
| `subscriber_count` | 订阅数。 |
| `photo_count` | 图片数量。 |
| `video_count` | 视频数量。 |
| `link_count` | 消息中的链接数量。 |
| `is_verified` | 账号是否已认证。 |
| `avatar_url` | 头像图片链接。 |
| `url` | 该记录在原平台上的可访问链接。 |
| `platform` | 数据来源平台标识，与请求里的 platform 一致（如 xiaohongshu、tiktok）。 |

完整参数和字段：<https://everyinfra.com/telegram-api/profile?utm_source=github&utm_medium=example_repo&utm_campaign=telegram-api>

#### `channel_posts`（频道帖子）

| 字段 | 含义 |
|---|---|
| `id` | 该记录在原平台上的唯一标识。 |
| `url` | 该记录在原平台上的可访问链接。 |
| `channel_username` | 频道用户名（@开头的公开标识）。 |
| `channel_title` | 频道名称。 |
| `text` | 正文内容，已去除 HTML 标签，全文返回、不截断（个别平台的列表结果本身只有摘要，以该平台的字段说明为准）。 |
| `view_count` | 浏览/播放数。 |
| `posted_at` | 发布时间，ISO 8601 格式、UTC 时区（如 2026-08-07T12:34:56+00:00）。 |
| `media_type` | 媒体类型（照片/视频/文件/语音）。 |
| `author` | 消息发送者。 |
| `platform` | 数据来源平台标识，与请求里的 platform 一致（如 xiaohongshu、tiktok）。 |
| `reactions` | 表情回应及各自数量。 |
| `media_url` | 媒体文件链接。 |
| `reply_to_url` | 被回复消息的链接。 |
| `is_forwarded` | 该消息是否为转发。 |

完整参数和字段：<https://everyinfra.com/telegram-api/channel_posts?utm_source=github&utm_medium=example_repo&utm_campaign=telegram-api>

#### `search`（关键词搜索）

| 字段 | 含义 |
|---|---|
| `id` | 该记录在原平台上的唯一标识。 |
| `url` | 该记录在原平台上的可访问链接。 |
| `text` | 正文内容，已去除 HTML 标签，全文返回、不截断（个别平台的列表结果本身只有摘要，以该平台的字段说明为准）。 |
| `posted_at` | 发布时间，ISO 8601 格式、UTC 时区（如 2026-08-07T12:34:56+00:00）。 |
| `view_count` | 浏览/播放数。 |
| `media_url` | 媒体文件链接。 |
| `channel_username` | 频道用户名（@开头的公开标识）。 |
| `channel_title` | 频道名称。 |
| `channel_type` | 类型（频道/群组/超级群）。 |
| `channel_subscriber_count` | 频道订阅数。 |
| `channel_description` | 频道简介。 |
| `platform` | 数据来源平台标识，与请求里的 platform 一致（如 xiaohongshu、tiktok）。 |

完整参数和字段：<https://everyinfra.com/telegram-api/search?utm_source=github&utm_medium=example_repo&utm_campaign=telegram-api>

### 常见问题

**调用时要不要提供 Telegram 账号或 Cookie？**

不用，请求头带 `Authorization: Bearer` 和 API Key 就能调，请求体写 `platform`、`action` 和能力参数。不用扫码、维护登录状态，也不用开浏览器。

**怎么收费？失败了收不收钱？有免费额度吗？**

按调用次数计费，每千次 $0.56 起。失败、空结果、参数错误和鉴权失败都不收费。新账号有 $1 试用额度，24 小时内有效，不用信用卡，领取方式见定价页 <https://everyinfra.com/pricing?utm_source=github&utm_medium=example_repo&utm_campaign=telegram-api>

**能把 Telegram 接口接进 Claude、Cursor 吗？**

能，远程 MCP 地址是 <https://api.everyinfra.com/mcp>，请求头加 `Authorization: Bearer` 和 API Key，不用装本地程序。Claude、Cursor、ChatGPT、Claude Code 配置见 <https://everyinfra.com/mcp-server?utm_source=github&utm_medium=example_repo&utm_campaign=telegram-api>。

**用 Telegram 数据要注意哪些合规问题？**

EveryInfra 服务条款要求你自行确保数据用法符合适用法律和相关平台条款，禁止用于违法、侵犯隐私或知识产权，或批量抓取用于骚扰、欺诈等恶意用途。用到昵称、头像等个人信息时，只留业务用得上的字段。

**可以拿到 Telegram 的哪些数据？**

Telegram 有 6 个能力：频道帖子、主页或对象详情、关键词搜索、群组资料、成员列表、内容详情。每个能力的参数和返回字段见平台页 <https://everyinfra.com/telegram-api?utm_source=github&utm_medium=example_repo&utm_campaign=telegram-api>

### 实测记录

发布前用本仓的代码对线上接口跑过一遍，命令就是「快速开始」里的 3 条。

| 命令 | 时间（新加坡时间） | 返回条数 | 扣费 |
|---|---|---|---|
| `python main.py channel durov` | 2026-11-25 15:32 | 1 | $0.000556 |
| `python main.py posts durov --out posts.csv` | 2026-11-25 13:21 | 20 | $0.000556 |
| `python main.py search bitcoin --out messages.csv` | 2026-11-25 13:21 | 20 | $0.000556 |

`profile` 返回的一条（正文截到 60 字，作者字段没放进来）：

```json
{
  "subscriber_count": 9873301,
  "photo_count": 106,
  "video_count": 47,
  "link_count": 203
}
```

## License

MIT
