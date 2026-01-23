import React, { FC, useState, useEffect, useRef } from 'react'
import { Home, History as HistoryIcon, ChevronLeft, SlidersHorizontal } from 'lucide-react'
import { useTaskStore } from '@/store/taskStore'
import { Link } from 'react-router-dom'
import { cn } from '@/lib/utils'

interface IProps {
    NoteForm: React.ReactNode
    Preview: React.ReactNode
    History: React.ReactNode
}

const MobileHomeLayout: FC<IProps> = ({ NoteForm, Preview, History }) => {
    const [activeTab, setActiveTab] = useState<'home' | 'history'>('history')
    const [showPreview, setShowPreview] = useState(false)
    const { currentTaskId, syncTasksWithServer } = useTaskStore()
    const isFirstRun = useRef(true)

    useEffect(() => {
        // Only jump to preview if it's NOT the first mount
        // This ensures "History" shows by default on load
        if (isFirstRun.current) {
            isFirstRun.current = false
            return
        }

        if (currentTaskId) {
            setShowPreview(true)
        }
    }, [currentTaskId])

    if (showPreview) {
        return (
            <div className="flex h-screen w-full flex-col bg-white">
                <div className="flex h-12 w-full items-center border-b border-gray-100 bg-white px-4">
                    <button
                        onClick={() => setShowPreview(false)}
                        className="flex items-center text-gray-600 hover:text-gray-900"
                    >
                        <ChevronLeft className="h-5 w-5" />
                        <span className="ml-1 text-sm font-medium">返回</span>
                    </button>
                </div>
                <div className="flex-1 overflow-hidden">
                    {Preview}
                </div>
            </div>
        )
    }

    return (
        <div className="flex h-screen w-full flex-col bg-gray-50">
            <main className="flex-1 overflow-hidden">
                {activeTab === 'home' && (
                    <div className="h-full overflow-y-auto p-4">
                        {/* Header for Home Tab with Settings */}
                        <div className="mb-6 flex items-center justify-between">
                            <Link to="/settings" className="p-2 -ml-2 text-gray-500 hover:text-primary transition-colors">
                                <SlidersHorizontal className="h-5 w-5" />
                            </Link>
                            <span className="absolute left-1/2 -translate-x-1/2 text-xl font-bold text-gray-800">BiliNote</span>
                            <div className="w-9" /> {/* Spacer for centering logo */}
                        </div>
                        {NoteForm}
                    </div>
                )}
                {activeTab === 'history' && (
                    <div className="h-full overflow-hidden bg-white">
                        {History}
                    </div>
                )}
            </main>

            <nav className="flex h-16 w-full items-center justify-around border-t border-gray-200 bg-white pb-safe">
                <button
                    onClick={() => setActiveTab('home')}
                    className={cn(
                        "flex flex-col items-center justify-center gap-1",
                        activeTab === 'home' ? "text-blue-600" : "text-gray-400"
                    )}
                >
                    <Home className="h-6 w-6" />
                    <span className="text-xs font-medium">生成</span>
                </button>

                <button
                    onClick={() => {
                        setActiveTab('history')
                        syncTasksWithServer()
                    }}
                    className={cn(
                        "flex flex-col items-center justify-center gap-1",
                        activeTab === 'history' ? "text-blue-600" : "text-gray-400"
                    )}
                >
                    <HistoryIcon className="h-6 w-6" />
                    <span className="text-xs font-medium">历史</span>
                </button>
            </nav>
        </div>
    )
}

export default MobileHomeLayout
