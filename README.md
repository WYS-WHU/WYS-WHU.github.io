# Yishan Wang — Academic Homepage

王一山的英文个人学术主页，采用桌面双栏与手机单栏布局。通过 GitHub Actions 构建并发布到 [GitHub Pages](https://wys-whu.github.io/)，仓库为 [WYS-WHU.github.io](https://github.com/WYS-WHU/WYS-WHU.github.io)。实际部署结果以仓库 Actions 为准。

逐栏目增删改文字、图片、论文作者与状态的完整说明见 **[主页维护教程.md](主页维护教程.md)**。

## 本地查看

在 `D:\My_Website_CV` 执行：

```powershell
python scripts/build_site.py
python scripts/preview_site.py
```

打开 `http://127.0.0.1:4173/`。前台运行时按 `Ctrl+C` 停止预览。服务仅提供 `dist/` 中的公开网页内容。也可以直接打开 `dist/index.html`，正文及相对路径资源无需服务器即可查看。构建使用 Python 标准库，字体均为本地文件。

## 从哪里修改

| 文件 | 用途 |
| --- | --- |
| `content/profile.json` | 姓名、邮箱、英文简介、教育、实习、项目、奖项、学生工作与兴趣，以及网站偏好 |
| `content/publications.json` | 四篇论文，含 Accepted 的 TC-SAR-Wave |
| `content/metrics.json` | ModelScope 累计下载／访问统计及核验时间；由刷新脚本生成 |
| `content/sources.json` | 内部来源索引，用于追溯材料与处理冲突，不是网站正文 |
| `assets/images/photo.png` | 当前照片，来自用户指定的根目录 `photo.png`；原图未改动 |
| `assets/images/publications/` | 从原论文提取的主模型／数据集框架图 |
| `CONTENT_REVIEW.md` | 本次整理结果、口径说明及待补充事项；是带日期的核对快照 |
| `scripts/refresh_metrics.py` | 重新获取公开统计，不下载数据集、不运行 Studio 推理 |
| `scripts/extract_publication_figures.py` | 从本地论文重新提取图，含明确页码与裁剪位置 |
| `site/index.template.html` | 页面结构与固定栏目文字 |
| `site/styles.css` / `site/main.js` | 响应式样式、手机菜单和论文图放大 |
| `scripts/build_site.py` / `scripts/preview_site.py` | 静态构建及本地预览 |
| `.github/workflows/pages.yml` | GitHub Pages 构建与部署工作流 |
| `work/` | 私有材料提取、网页快照、API 响应和图像核对记录；已加入 `.gitignore` |

`profile.json` 和 `publications.json` 是内容的唯一维护入口；核对快照不作为自动同步的数据源。未知值使用 JSON `null`，不能显示成 0、已发表或虚构链接。月份格式为 `YYYY-MM`，只有年份时保留 `YYYY`。

`sources` 数组关联 `sources.json` 中的编号。`verification`、`editorial_note`、`date_note`、`missing` 等是内部备注，后续网页只读取展示字段，不把这些备注直接展示给访客。

内容修改后运行 `python scripts/build_site.py` 并刷新浏览器。未来更换照片时更新 `assets/images/photo.png` 并重新构建。照片的裁剪在 CSS 中完成，不修改根目录原图。

## 更新下载与访问统计

在本目录执行：

```powershell
python scripts/refresh_metrics.py
python scripts/build_site.py
```

仅使用 Python 标准库。脚本读取数据集公开 API 和 Studio 页面内嵌的公开 JSON；两项都成功且身份匹配后才覆盖 `content/metrics.json`。失败会保留上一份统计，不能写入零值。原始响应保留在 `work/metrics/`。

本地预览服务启动时刷新一次，此后后台每 10 分钟刷新；网页前台每分钟读取 `/api/metrics` 缓存，切回页面也会读取。失败沿用最近成功数据，不归零。页面只显示统计及资源链接，不显示采集日期说明；日期保留在 JSON。下载次数、访问次数和独立用户数不能互换。直接打开静态 HTML 只有构建快照；GitHub Pages 工作流每 6 小时尝试获取一次计数、保存已验证快照并重新部署；失败保留上一份快照。定时任务由 GitHub 排队执行，可能延迟。手动运行部署工作流也会刷新计数。

## 论文维护规则

- MS²Gait：CVPR 2026，Shenyin Xu 与 Yishan Wang 共同一作。
- InterMC：Pattern Recognition **172 (2026), 112741**；在线日期为 **2025-11-20**，不与卷期年份混淆。
- TC-SAR-Coast：**ESSD Discussions preprint · Under review**，不是 ESSD 已接收／正式发表文章。
- TC-SAR-Wave：已接收（Accepted），显示七位作者，Yuting Zhu 为第一及通讯作者；没有编造文章链接。
- 当前展示四篇；TC-SAR-Wave 为 Accepted，TC-SAR-Coast 保持公开讨论中的预印本状态。共同一作标 `*`，通讯作者标 `†`。
- TC-SAR-Coast 是数据集论文，选用其构建流程图；其他三篇选用主模型图。图片来自原文，不重绘结构。

## 发布边界

公开邮箱为 **wang_ysys@163.com**。网站语言为英文。建议主页仓库为 `WYS-WHU.github.io`，地址为 `https://wys-whu.github.io/`；采用 GitHub Actions 发布，仅上传构建后的 dist。

生成的 `dist/` 只包含网页、样式、脚本、本地字体与许可及选用的图片（头像、四篇论文图、项目横幅和四个记录 logo）。重建会清理并重新生成 `dist/`。不要把此资料目录整体设为 GitHub Pages 发布目录；原始简历含手机号，PPT 包含其他私人信息。根目录原始 PDF、PPT、PNG、`work/`、内部 `content/sources.json`、`CONTENT_REVIEW.md` 以及工具截图和运行状态已加入 `.gitignore`；设计约定 sidecar `.impeccable/design.json` 可随源码维护。不要把来源索引和核对文档复制到公开网页目录。

## GitHub Pages 部署与后续更新

1. 将 `.github/`、`site/`、`scripts/build_site.py`、三个公开内容 JSON（profile、publications、metrics）、选用的 `assets/`、`.gitignore` 和本说明放入目标仓库。
2. 在仓库 **Settings → Pages → Build and deployment → Source** 选择 **GitHub Actions**。
3. 推送到 `main`，或在 Actions 手动运行 **Build and deploy academic homepage**。
4. 工作流先构建，再仅上传 `dist/`。以 GitHub Actions 部署完成状态和返回链接确认上线。

工作流按 [GitHub 官方说明](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages) 配置。发布已获用户明确授权。`PRODUCT.md` 和 `DESIGN.md` 记录后续维护约定，内容以 JSON 为准。

## 当前仍待补充

1. 可选：TC-SAR-Wave 公开文章／数据链接，待提供后补充。
2. 可选：Google Scholar／ORCID、未确定的其他奖项年份、比赛证书或现场照片、适合公开下载的精简 CV。没有这些也可继续制作主页。

本科专业已从现有自我介绍 PPT 的第 4 页识别为“电子信息工程”，无需重新提供。清华项目正式中文名已在官网核验；英文项目名目前是编辑翻译。

### 修改后的上传命令

先修改源文件并运行构建确认，然后执行（新增图片需按 `.gitignore` 中的白名单添加路径，不能上传原始私人材料）：

```powershell
git add -u
git commit -m "Update academic homepage"
git pull --rebase origin main
git push origin main
```

GitHub Actions 定时任务可能已更新 `content/metrics.json`，所以推送前需要拉取远端提交。不要强制推送覆盖远端。部署与计数刷新均使用 GitHub 自带的 `GITHUB_TOKEN`，不需要把个人 Token 写入仓库。
