import { Trash, Search } from 'lucide-react'
import { useTaskStore } from '@/store/taskStore'
import { cn } from '@/lib/utils.ts'
import { Button } from '@/components/ui/button.tsx'
import LazyImage from "@/components/LazyImage.tsx";
import { FC, useState } from 'react'

interface NoteHistoryProps {
  onSelect: (taskId: string) => void
  selectedId: string | null
}

const NoteHistory: FC<NoteHistoryProps> = ({ onSelect, selectedId }) => {
  const tasks = useTaskStore(state => state.tasks)
  const removeTask = useTaskStore(state => state.removeTask)
  const baseURL = (String(import.meta.env.VITE_API_BASE_URL || 'api')).replace(/\/$/, '')
  const [search, setSearch] = useState('')

  const filteredTasks = search.trim()
    ? tasks.filter(task => task.audioMeta.title?.toLowerCase().includes(search.toLowerCase()))
    : tasks

  if (filteredTasks.length === 0) {
    return (
      <div className="p-4">
        <div className="relative mb-4">
          <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-neutral-400" />
          <input
            type="text"
            placeholder="搜索笔记标题..."
            className="w-full rounded-full bg-neutral-100 border-none px-10 py-2 text-sm outline-none focus:ring-2 focus:ring-primary/20"
            value={search}
            onChange={e => setSearch(e.target.value)}
          />
        </div>
        <div className="rounded-xl border border-dashed border-neutral-200 py-10 text-center">
          <p className="text-sm text-neutral-500">没发现相关的笔记呢~</p>
        </div>
      </div>
    )
  }

  return (
    <div className="p-4">
      <div className="relative mb-4">
        <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-neutral-400" />
        <input
          type="text"
          placeholder="搜索笔记标题..."
          className="w-full rounded-full bg-neutral-100 border-none px-10 py-2 text-sm outline-none focus:ring-2 focus:ring-primary/20"
          value={search}
          onChange={e => setSearch(e.target.value)}
        />
      </div>
      <div className="flex flex-col gap-3">
        {filteredTasks.map(task => {
          const dateObj = new Date(task.createdAt);
          const formattedDate = task.createdAt
            ? `${(dateObj.getMonth() + 1).toString().padStart(2, '0')}-${dateObj.getDate().toString().padStart(2, '0')}`
            : '';

          return (
            <div
              key={task.id}
              onClick={() => onSelect(task.id)}
              className={cn(
                'flex cursor-pointer flex-col rounded-xl border border-neutral-200 p-3 transition-all active:scale-[0.98]',
                selectedId === task.id ? 'border-primary bg-primary-light ring-1 ring-primary/20' : 'bg-white shadow-sm'
              )}
            >
              <div className="flex items-start gap-3">
                <div className="relative shrink-0">
                  {task.platform === 'local' ? (
                    <img
                      src={task.audioMeta.cover_url ? `${task.audioMeta.cover_url}` : '/placeholder.png'}
                      alt="封面"
                      className="h-16 w-20 rounded-lg object-cover shadow-sm"
                    />
                  ) : (
                    <div className="h-16 w-20 overflow-hidden rounded-lg shadow-sm">
                      <LazyImage
                        src={task.audioMeta.cover_url
                          ? `${baseURL}/image_proxy?url=${encodeURIComponent(task.audioMeta.cover_url)}`
                          : '/placeholder.png'
                        }
                        alt="封面"
                        className="h-full w-full"
                      />
                    </div>
                  )}
                </div>

                <div className="flex min-w-0 flex-1 flex-col justify-between self-stretch">
                  <div className="line-clamp-2 text-sm font-medium leading-snug text-neutral-900">
                    {task.audioMeta.title || '未命名笔记'}
                  </div>

                  <div className="mt-2 flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <span className="text-[10px] text-neutral-400">{formattedDate}</span>
                      {task.status === 'SUCCESS' && (
                        <div className="rounded-full bg-green-100 px-2 py-0.5 text-[10px] font-medium text-green-700">
                          已完成
                        </div>
                      )}
                      {task.status === 'FAILED' && (
                        <div className="rounded-full bg-red-100 px-2 py-0.5 text-[10px] font-medium text-red-700">
                          失败
                        </div>
                      )}
                      {(task.status !== 'SUCCESS' && task.status !== 'FAILED') && (
                        <div className="rounded-full bg-blue-100 px-2 py-0.5 text-[10px] font-medium text-blue-700">
                          处理中
                        </div>
                      )}
                    </div>

                    <Button
                      type="button"
                      size="icon"
                      variant="ghost"
                      onClick={e => {
                        e.stopPropagation()
                        removeTask(task.id)
                      }}
                      className="h-7 w-7 rounded-full text-neutral-400 hover:bg-red-50 hover:text-red-500"
                    >
                      <Trash className="h-3.5 w-3.5" />
                    </Button>
                  </div>
                </div>
              </div>
            </div>
          )
        })}
      </div>
    </div>
  )
}

export default NoteHistory
