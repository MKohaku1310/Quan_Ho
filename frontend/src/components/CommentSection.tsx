import { useState } from "react";
import { useAuth, type Comment } from "@/contexts/AuthContext";
import { MessageSquare, Edit2, Trash2, Send, X, Check } from "lucide-react";
import { z } from "zod";
import { useTranslation } from "react-i18next";

interface CommentSectionProps {
  targetType: Comment["targetType"];
  targetId: number;
}

export default function CommentSection({ targetType, targetId }: CommentSectionProps) {
  const { t } = useTranslation();
  const { user, isAuthenticated, getComments, addComment, editComment, deleteComment, setShowLoginModal } = useAuth();
  
  const commentSchema = z.string().trim().min(1, t("comments.empty_error")).max(1000, t("comments.max_error"));
  
  const comments = getComments(targetType, targetId);
  const [newComment, setNewComment] = useState("");
  const [editingId, setEditingId] = useState<number | null>(null);
  const [editContent, setEditContent] = useState("");
  const [error, setError] = useState("");

  // Xử lý gửi bình luận mới
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    const result = commentSchema.safeParse(newComment);
    if (!result.success) {
      setError(result.error.errors[0].message);
      return;
    }
    addComment(targetType, targetId, result.data);
    setNewComment("");
  };

  // Xử lý chỉnh sửa bình luận
  const handleEdit = (commentId: number) => {
    const result = commentSchema.safeParse(editContent);
    if (!result.success) return;
    editComment(commentId, result.data);
    setEditingId(null);
  };

  return (
    <div className="mt-10">
      <h2 className="mb-6 flex items-center gap-2 font-display text-xl font-semibold text-foreground">
        <MessageSquare className="h-5 w-5 text-primary" />
        {t("comments.title")} ({comments.length})
      </h2>

      {/* Form bình luận mới */}
      {isAuthenticated ? (
        <form onSubmit={handleSubmit} className="mb-6">
          <div className="flex gap-3">
            <img src={user?.avatar} alt="" className="h-9 w-9 flex-shrink-0 rounded-full object-cover" />
            <div className="flex-1">
              <textarea
                value={newComment}
                onChange={(e) => {
                  setNewComment(e.target.value);
                  setError("");
                }}
                placeholder={t("comments.placeholder")}
                rows={3}
                className="w-full rounded-md border border-input bg-background px-3 py-2 text-sm text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring resize-none"
              />
              {error && <p className="mt-1 text-xs text-destructive">{error}</p>}
              <div className="mt-2 flex justify-between items-center">
                <span className="text-xs text-muted-foreground">{newComment.length}/1000</span>
                <button
                  type="submit"
                  disabled={!newComment.trim()}
                  className="flex items-center gap-1.5 rounded-md bg-primary px-4 py-1.5 text-sm font-medium text-primary-foreground transition-colors hover:bg-primary/90 disabled:opacity-50"
                >
                  <Send className="h-3.5 w-3.5" /> {t("comments.send")}
                </button>
              </div>
            </div>
          </div>
        </form>
      ) : (
        <div className="mb-6 rounded-lg border border-border bg-muted p-4 text-center">
          <p className="text-sm text-muted-foreground">
            <button onClick={() => setShowLoginModal(true)} className="font-medium text-primary hover:underline">
              {t("nav.login")}
            </button>{" "}
            {t("comments.login_to_comment")}
          </p>
        </div>
      )}

      {/* Danh sách bình luận */}
      {comments.length > 0 ? (
        <div className="space-y-4">
          {comments.map((comment) => (
            <div key={comment.id} className="flex gap-3 rounded-lg border border-border bg-card p-4 shadow-card">
              <img src={comment.avatar} alt="" className="h-9 w-9 flex-shrink-0 rounded-full object-cover" />
              <div className="min-w-0 flex-1">
                <div className="flex items-center gap-2">
                  <span className="text-sm font-semibold text-foreground">{comment.username}</span>
                  <span className="text-xs text-muted-foreground">
                    {new Date(comment.createdAt).toLocaleDateString("vi-VN")}
                  </span>
                </div>

                {editingId === comment.id ? (
                  <div className="mt-2">
                    <textarea
                      value={editContent}
                      onChange={(e) => setEditContent(e.target.value)}
                      rows={2}
                      className="w-full rounded-md border border-input bg-background px-3 py-2 text-sm text-foreground focus:outline-none focus:ring-2 focus:ring-ring resize-none"
                    />
                    <div className="mt-1 flex gap-2">
                      <button
                        onClick={() => handleEdit(comment.id)}
                        className="flex items-center gap-1 rounded-md bg-primary px-3 py-1 text-xs text-primary-foreground"
                      >
                        <Check className="h-3 w-3" /> {t("comments.save")}
                      </button>
                      <button
                        onClick={() => setEditingId(null)}
                        className="flex items-center gap-1 rounded-md bg-muted px-3 py-1 text-xs text-muted-foreground"
                      >
                        <X className="h-3 w-3" /> {t("comments.cancel")}
                      </button>
                    </div>
                  </div>
                ) : (
                  <p className="mt-1 text-sm text-muted-foreground">{comment.content}</p>
                )}

                {/* Hành động sửa/xóa cho bình luận của chính mình */}
                {user && comment.userId === user.id && editingId !== comment.id && (
                  <div className="mt-2 flex gap-3">
                    <button
                      onClick={() => {
                        setEditingId(comment.id);
                        setEditContent(comment.content);
                      }}
                      className="flex items-center gap-1 text-xs text-muted-foreground hover:text-primary"
                    >
                      <Edit2 className="h-3 w-3" /> {t("comments.edit")}
                    </button>
                    <button
                      onClick={() => deleteComment(comment.id)}
                      className="flex items-center gap-1 text-xs text-muted-foreground hover:text-destructive"
                    >
                      <Trash2 className="h-3 w-3" /> {t("comments.delete")}
                    </button>
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      ) : (
        <p className="py-8 text-center text-sm text-muted-foreground">
          {t("comments.no_comments")}
        </p>
      )}
    </div>
  );
}
