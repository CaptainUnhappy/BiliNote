# BiliNote 移动端前端重构方案 (Mobile Redesign Plan)

## 1. 核心目标
将现有的桌面端优先（Desktop-First）布局转变为**响应式设计（Responsive Design）**，确保在手机浏览器及 PWA（渐进式 Web 应用）环境下拥有原生 App 般的交互体验。

## 2. 布局调整策略 (Responsive Layout)

### 2.1 导航模式切换
*   **桌面端 (≥ 768px)**：保留现有的左侧常驻侧边栏。
*   **移动端 (< 768px)**：
    *   **隐藏侧边栏**：侧边栏改为从左侧滑出的抽屉（Drawer）或完全移除。
    *   **底部导航栏 (Bottom Navigation)**：在屏幕底部固定三个图标入口：
        1. **首页 (Home)**：URL 输入与生成。
        2. **历史 (History)**：笔记列表。
        3. **设置 (Settings)**：模型与配置。

### 2.2 笔记列表改造
*   **卡片化设计**：将列表项改为高度适中的卡片，包含视频封面缩略图、标题、平台图标和生成时间。
*   **交互优化**：增加点击热区，支持长按或侧滑调出“删除”操作。

### 2.3 内容查看器
*   **双栏转单栏**：在手机端，Markdown 预览和原文转录不再分左右两栏展示，而是改为“标签页 (Tabs)”切换模式或上下堆叠。
*   **图片缩放**：笔记中的截图支持点击后全屏预览，并支持手势缩放。

## 3. 关键交互组件优化

| 桌面端组件 | 移动端适配建议 | 推荐库 |
| :--- | :--- | :--- |
| **Dialog (对话框)** | **Bottom Sheet (底部抽屉)** | [Vaul](https://github.com/emilkowalski/vaul) |
| **Sidebar (侧边栏)** | **Navigation Bar (底部导航)** | Tailwind CSS |
| **Select (下拉框)** | **Picker (原生感滚轮/抽屉列表)** | Radix UI / Shadcn |
| **Toast (通知)** | **移动端顶部/中间轻量提示** | React Hot Toast |

## 4. PWA (Progressive Web App) 支持
通过 PWA 技术让用户将网页“安装”到手机桌面：
1.  **Manifest 配置**：设置 `manifest.json`，定义图标、启动页背景色及 `display: standalone`（隐藏浏览器地址栏）。
2.  **Service Worker**：实现基础的资源缓存，提升弱网环境下的首屏加载速度。
3.  **图标设计**：提供 192x192 和 512x512 尺寸的圆角图标。

## 5. 实施路线图

### 第一阶段：响应式骨架改造
*   修改 `Index.tsx`：引入 MediaQuery 监听，动态切换 `Sidebar` 和 `BottomNav`。
*   适配 `App.css`：确保容器宽度在手机端为 100%。

### 第二阶段：表单与交互优化
*   将 `NoteForm` 改造为底部滑出的抽屉，优化 URL 粘贴体验。
*   适配 `MarkdownViewer`：优化移动端字号、行高及图片边距。

### 第三阶段：PWA 与体验增强
*   添加 PWA 相关配置文件。
*   添加页面切换动效 (Framer Motion)。

---
*此方案已由 AI 助手整理，随时可开始执行第一阶段任务。*
