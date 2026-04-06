import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { Toaster } from "@/components/ui/toaster";
import { TooltipProvider } from "@/components/ui/tooltip";
import { AuthProvider } from "@/contexts/AuthContext";
import LoginModal from "@/components/LoginModal";
import ChatBot from "@/components/ChatBot";
import Index from "./pages/Index";
import Introduction from "./pages/Introduction";
import Songs from "./pages/Songs";
import SongDetail from "./pages/SongDetail";
import Artists from "./pages/Artists";
import ArtistDetail from "./pages/ArtistDetail";
import Villages from "./pages/Villages";
import News from "./pages/News";
import NewsDetail from "./pages/NewsDetail";
import EventDetail from "./pages/EventDetail";
import Register from "./pages/Register";
import Profile from "./pages/Profile";
import NotFound from "./pages/NotFound";
import AddArtist from "./pages/AddArtist";
import AddSong from "./pages/AddSong";

const queryClient = new QueryClient();

const App = () => (
  <QueryClientProvider client={queryClient}>
    <TooltipProvider>
      <Toaster />
      <Sonner />
      <BrowserRouter>
        <AuthProvider>
          <LoginModal />
          <ChatBot />
          <Routes>
            <Route path="/" element={<Index />} />
            <Route path="/gioi-thieu" element={<Introduction />} />
            <Route path="/bai-hat" element={<Songs />} />
            <Route path="/bai-hat/:id" element={<SongDetail />} />
            <Route path="/nghe-nhan" element={<Artists />} />
            <Route path="/nghe-nhan/:id" element={<ArtistDetail />} />
            <Route path="/lang-quan-ho" element={<Villages />} />
            <Route path="/tin-tuc" element={<News />} />
            <Route path="/tin-tuc/:id" element={<NewsDetail />} />
            <Route path="/su-kien/:id" element={<EventDetail />} />
            <Route path="/dang-ky" element={<Register />} />
            <Route path="/ho-so" element={<Profile />} />
            <Route path="/them-nghe-nhan" element={<AddArtist />} />
            <Route path="/them-bai-hat" element={<AddSong />} />
            <Route path="*" element={<NotFound />} />
          </Routes>
        </AuthProvider>
      </BrowserRouter>
    </TooltipProvider>
  </QueryClientProvider>
);

export default App;
