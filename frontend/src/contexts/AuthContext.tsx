import { createContext, useContext, useState, useCallback, useEffect, type ReactNode } from "react";
import { toast } from "sonner";

export interface User {
  id: number;
  username: string;
  email: string;
  avatar: string;
  role: "user" | "admin";
  joinedDate: string;
}

export interface Comment {
  id: number;
  userId: number;
  username: string;
  avatar: string;
  targetType: "song" | "article" | "event";
  targetId: number;
  content: string;
  createdAt: string;
  updatedAt: string;
}

interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<boolean>;
  register: (username: string, email: string, password: string) => Promise<boolean>;
  logout: () => void;
  updateProfile: (data: Partial<User>) => void;
  favorites: number[];
  toggleFavorite: (songId: number) => void;
  isFavorite: (songId: number) => boolean;
  comments: Comment[];
  addComment: (targetType: Comment["targetType"], targetId: number, content: string) => void;
  editComment: (commentId: number, content: string) => void;
  deleteComment: (commentId: number) => void;
  getComments: (targetType: Comment["targetType"], targetId: number) => Comment[];
  showLoginModal: boolean;
  setShowLoginModal: (show: boolean) => void;
}

const AuthContext = createContext<AuthContextType | null>(null);

// Mock user database for demo
const MOCK_USERS: (User & { password: string })[] = [
  {
    id: 1,
    username: "quanho_lover",
    email: "user@example.com",
    password: "password123",
    avatar: "https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?w=100",
    role: "user",
    joinedDate: "2025-06-15",
  },
  {
    id: 2,
    username: "admin",
    email: "admin@example.com",
    password: "admin123",
    avatar: "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=100",
    role: "admin",
    joinedDate: "2024-01-01",
  },
];

const MOCK_COMMENTS: Comment[] = [
  {
    id: 1,
    userId: 1,
    username: "quanho_lover",
    avatar: "https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?w=100",
    targetType: "song",
    targetId: 1,
    content: "Bài hát này thật hay! Giọng hát của NSND Thúy Cải luôn khiến tôi xúc động.",
    createdAt: "2026-03-10T10:30:00Z",
    updatedAt: "2026-03-10T10:30:00Z",
  },
  {
    id: 2,
    userId: 1,
    username: "quanho_lover",
    avatar: "https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?w=100",
    targetType: "song",
    targetId: 1,
    content: "Tôi đã nghe bài này hàng trăm lần mà không bao giờ chán.",
    createdAt: "2026-03-11T14:00:00Z",
    updatedAt: "2026-03-11T14:00:00Z",
  },
];

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [favorites, setFavorites] = useState<number[]>([]);
  const [comments, setComments] = useState<Comment[]>(MOCK_COMMENTS);
  const [showLoginModal, setShowLoginModal] = useState(false);

  // Restore session on mount
  useEffect(() => {
    const token = localStorage.getItem("jwt_token");
    const savedUser = localStorage.getItem("user_data");
    const savedFavorites = localStorage.getItem("favorites");
    if (token && savedUser) {
      try {
        setUser(JSON.parse(savedUser));
      } catch {
        localStorage.removeItem("jwt_token");
        localStorage.removeItem("user_data");
      }
    }
    if (savedFavorites) {
      try {
        setFavorites(JSON.parse(savedFavorites));
      } catch {
        // ignore
      }
    }
    setIsLoading(false);
  }, []);

  // Persist favorites
  useEffect(() => {
    if (user) {
      localStorage.setItem("favorites", JSON.stringify(favorites));
    }
  }, [favorites, user]);

  const login = useCallback(async (email: string, password: string): Promise<boolean> => {
    // Simulate API call: POST /auth/login
    await new Promise((r) => setTimeout(r, 800));
    const found = MOCK_USERS.find((u) => u.email === email && u.password === password);
    if (!found) {
      toast.error("Email hoặc mật khẩu không đúng");
      return false;
    }
    const { password: _, ...userData } = found;
    const fakeToken = btoa(JSON.stringify({ userId: found.id, exp: Date.now() + 86400000 }));
    localStorage.setItem("jwt_token", fakeToken);
    localStorage.setItem("user_data", JSON.stringify(userData));
    setUser(userData);
    toast.success(`Chào mừng ${userData.username}!`);
    return true;
  }, []);

  const register = useCallback(async (username: string, email: string, password: string): Promise<boolean> => {
    // Simulate API call: POST /auth/register
    await new Promise((r) => setTimeout(r, 800));
    if (MOCK_USERS.some((u) => u.email === email)) {
      toast.error("Email đã được sử dụng");
      return false;
    }
    const newUser: User = {
      id: Date.now(),
      username,
      email,
      avatar: `https://ui-avatars.com/api/?name=${encodeURIComponent(username)}&background=8b2500&color=fff`,
      role: "user",
      joinedDate: new Date().toISOString().split("T")[0],
    };
    const fakeToken = btoa(JSON.stringify({ userId: newUser.id, exp: Date.now() + 86400000 }));
    localStorage.setItem("jwt_token", fakeToken);
    localStorage.setItem("user_data", JSON.stringify(newUser));
    setUser(newUser);
    toast.success("Đăng ký thành công!");
    return true;
  }, []);

  const logout = useCallback(() => {
    localStorage.removeItem("jwt_token");
    localStorage.removeItem("user_data");
    localStorage.removeItem("favorites");
    setUser(null);
    setFavorites([]);
    toast.success("Đã đăng xuất");
  }, []);

  const updateProfile = useCallback((data: Partial<User>) => {
    setUser((prev) => {
      if (!prev) return prev;
      const updated = { ...prev, ...data };
      localStorage.setItem("user_data", JSON.stringify(updated));
      return updated;
    });
    toast.success("Cập nhật hồ sơ thành công!");
  }, []);

  const toggleFavorite = useCallback((songId: number) => {
    if (!user) {
      setShowLoginModal(true);
      return;
    }
    setFavorites((prev) => {
      if (prev.includes(songId)) {
        toast.success("Đã xóa khỏi yêu thích");
        return prev.filter((id) => id !== songId);
      }
      toast.success("Đã thêm vào yêu thích");
      return [...prev, songId];
    });
  }, [user]);

  const isFavorite = useCallback((songId: number) => favorites.includes(songId), [favorites]);

  const addComment = useCallback((targetType: Comment["targetType"], targetId: number, content: string) => {
    if (!user) return;
    const newComment: Comment = {
      id: Date.now(),
      userId: user.id,
      username: user.username,
      avatar: user.avatar,
      targetType,
      targetId,
      content,
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
    };
    setComments((prev) => [newComment, ...prev]);
    toast.success("Bình luận đã được đăng!");
  }, [user]);

  const editComment = useCallback((commentId: number, content: string) => {
    setComments((prev) =>
      prev.map((c) =>
        c.id === commentId ? { ...c, content, updatedAt: new Date().toISOString() } : c
      )
    );
    toast.success("Đã cập nhật bình luận");
  }, []);

  const deleteComment = useCallback((commentId: number) => {
    setComments((prev) => prev.filter((c) => c.id !== commentId));
    toast.success("Đã xóa bình luận");
  }, []);

  const getComments = useCallback(
    (targetType: Comment["targetType"], targetId: number) =>
      comments.filter((c) => c.targetType === targetType && c.targetId === targetId),
    [comments]
  );

  return (
    <AuthContext.Provider
      value={{
        user,
        isAuthenticated: !!user,
        isLoading,
        login,
        register,
        logout,
        updateProfile,
        favorites,
        toggleFavorite,
        isFavorite,
        comments,
        addComment,
        editComment,
        deleteComment,
        getComments,
        showLoginModal,
        setShowLoginModal,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) throw new Error("useAuth must be used within AuthProvider");
  return context;
}
