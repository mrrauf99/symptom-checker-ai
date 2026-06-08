import { useState, useEffect, useRef } from "react";
import { useParams, useNavigate, useOutletContext } from "react-router-dom";
import { chatAPI } from "../../api/chatAPI.js";
import { messagesAPI } from "../../api/messagesAPI.js";
import { sessionsAPI } from "../../api/sessionsAPI.js";
import { getErrorMessage } from "../../utils/helpers.js";
import { Send, Bot } from "../../components/layout/icons.jsx";
import Spinner from "../../components/ui/Spinner.jsx";
import PredictionResponse from "../../components/prediction/PredictionResponse.jsx";
import AnalyzingMessage from "../../components/prediction/AnalyzingMessage.jsx";
import toast from "react-hot-toast";

function TypingIndicator() {
  return <AnalyzingMessage />;
}

function Message({ msg }) {
  const isUser = msg.role === "user";
  return (
    <div
      className={`flex items-end gap-3 animate-slide-up ${isUser ? "flex-row-reverse" : ""}`}
    >
      {/* Avatar */}
      <div
        className={`w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 ${
          isUser ? "bg-slate-200 text-slate-600" : "bg-mint-100 text-mint-600"
        }`}
      >
        {isUser ? (
          <span className="text-xs font-display font-semibold">You</span>
        ) : (
          <Bot size={14} />
        )}
      </div>

      {/* Content */}
      <div
        className={`max-w-full sm:max-w-[72%] ${isUser ? "items-end" : "items-start"} flex flex-col`}
      >
        {isUser ? (
          // User message - simple bubble
          <div className="px-4 py-3 rounded-2xl text-sm font-body leading-relaxed bg-mint-500 text-white rounded-br-sm shadow-card">
            {msg.content}
          </div>
        ) : // AI response - use new prediction response component if we have prediction data
        msg.prediction_data ? (
          <PredictionResponse data={msg.prediction_data} />
        ) : (
          // Fallback to simple text if no prediction data
          <div className="bg-white border border-slate-100 rounded-2xl rounded-bl-sm px-4 py-3 shadow-card text-sm font-body leading-relaxed text-slate-800">
            {msg.content}
          </div>
        )}
      </div>
    </div>
  );
}

function EmptyChat() {
  const suggestions = [
    "I have fever and headache for 3 days",
    "I feel nauseous and have body pain",
    "I have a persistent cough and sore throat",
    "My stomach hurts and I feel weak",
  ];
  return (
    <div className="flex-1 flex flex-col items-center justify-center p-8 text-center">
      <div className="w-16 h-16 rounded-2xl bg-mint-100 flex items-center justify-center mb-4">
        <Bot size={28} className="text-mint-600" />
      </div>
      <h2 className="font-display font-bold text-slate-800 text-xl mb-2">
        MediSense AI is ready
      </h2>
      <p className="text-slate-500 font-body text-sm mb-6 max-w-xs">
        Describe your symptoms in natural language and I'll help identify
        possible conditions.
      </p>
      <p className="text-xs font-display font-semibold text-slate-400 uppercase tracking-wider mb-3">
        Try asking
      </p>
      <div className="flex flex-col gap-2 w-full max-w-sm">
        {suggestions.map((s) => (
          <button
            key={s}
            className="text-left px-4 py-2.5 rounded-xl bg-white border border-slate-200
              hover:border-mint-300 hover:bg-mint-50 text-sm text-slate-600 font-body
              transition-all duration-200"
            onClick={() => {
              const el = document.getElementById("chat-input");
              if (el) {
                el.value = s;
                el.dispatchEvent(new Event("input", { bubbles: true }));
                el.focus();
              }
            }}
          >
            {s}
          </button>
        ))}
      </div>
    </div>
  );
}

export default function ChatPage() {
  const { sessionId } = useParams();
  const navigate = useNavigate();
  const { refreshSessions } = useOutletContext() || {};

  const [messages, setMessages] = useState([]);
  const [sessionDetails, setSessionDetails] = useState(null);
  const [input, setInput] = useState("");
  const [sending, setSending] = useState(false);
  const [loadingMessages, setLoadingMessages] = useState(false);
  const [activeSession, setActiveSession] = useState(sessionId || null);

  const bottomRef = useRef(null);
  const inputRef = useRef(null);
  const messagesContainerRef = useRef(null);
  const hasUserMessagesRef = useRef(false);
  const userScrolledRef = useRef(false);

  // Load messages and session when session changes
  useEffect(() => {
    if (!sessionId) {
      setMessages([]);
      setSessionDetails(null);
      setActiveSession(null);
      return;
    }
    setActiveSession(sessionId);
    const fetchMessagesAndSession = async () => {
      setLoadingMessages(true);
      try {
        const [msgData, sessionData] = await Promise.all([
          messagesAPI.getSessionMessages(sessionId),
          sessionsAPI.getSession(sessionId),
        ]);
        const mapped = msgData.map((m, i) => ({
          id: i,
          role: m.role,
          content: m.content,
          prediction_data: m.prediction_data,
        }));
        setMessages(mapped);
        setSessionDetails(sessionData);
        // If this is an existing session with messages, mark it as having user messages
        if (mapped.some((m) => m.role === "user")) {
          hasUserMessagesRef.current = true;
        }
      } catch {
        toast.error("Could not load session details");
      } finally {
        setLoadingMessages(false);
      }
    };
    fetchMessagesAndSession();
  }, [sessionId]);

  // Smart auto scroll - only scroll if user is near bottom or no scrolling has happened yet
  useEffect(() => {
    if (!messagesContainerRef.current) return;

    const container = messagesContainerRef.current;
    const isNearBottom =
      container.scrollHeight - container.scrollTop - container.clientHeight <
      150;

    // Auto scroll only on first message or if user is already scrolled near the bottom
    if (isNearBottom || messages.length === 0) {
      setTimeout(() => {
        bottomRef.current?.scrollIntoView({ behavior: "smooth" });
      }, 0);
      userScrolledRef.current = false;
    }
  }, [messages]);

  // Track manual scrolling
  useEffect(() => {
    const container = messagesContainerRef.current;
    if (!container) return;

    const handleScroll = () => {
      const isNearBottom =
        container.scrollHeight - container.scrollTop - container.clientHeight <
        150;
      userScrolledRef.current = !isNearBottom;
    };

    container.addEventListener("scroll", handleScroll);
    return () => container.removeEventListener("scroll", handleScroll);
  }, []);

  // Cleanup empty sessions on unmount
  useEffect(() => {
    return () => {
      // Only delete sessions that were NEWLY created (not from URL) and have NO user messages
      if (activeSession && !sessionId && !hasUserMessagesRef.current) {
        sessionsAPI
          .deleteSession(activeSession)
          .then(() => {
            refreshSessions?.();
          })
          .catch(() => {
            // Silent fail for cleanup
          });
      }
    };
  }, [activeSession, sessionId, refreshSessions]);

  const handleSend = async () => {
    const text = input.trim();
    if (!text || sending) return;

    let currentSessionId = activeSession;

    // Create a session if none exists
    if (!currentSessionId) {
      try {
        const title = text.slice(0, 40) + (text.length > 40 ? "..." : "");
        const { session_id } = await sessionsAPI.createSession(title);
        refreshSessions?.();
        currentSessionId = session_id;
        setActiveSession(session_id);
        navigate(`/chat/${session_id}`, { replace: true });
      } catch {
        toast.error("Could not start session");
        return;
      }
    }

    // Mark that user has sent a message
    hasUserMessagesRef.current = true;

    // Optimistic user message
    const userMsg = { id: Date.now(), role: "user", content: text };
    setMessages((prev) => [...prev, userMsg]);
    setInput("");
    setSending(true);

    try {
      const res = await chatAPI.sendMessage({
        session_id: currentSessionId,
        content: text,
      });

      const aiMsg = {
        id: Date.now() + 1,
        role: "assistant",
        content: res.response,
        prediction_data: res,
      };
      setMessages((prev) => [...prev, aiMsg]);
    } catch (err) {
      toast.error(getErrorMessage(err));
      // Remove optimistic message on failure
      setMessages((prev) => prev.filter((m) => m.id !== userMsg.id));
      setInput(text);
    } finally {
      setSending(false);
      inputRef.current?.focus();
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleEndSession = async () => {
    if (!activeSession) return;
    try {
      await sessionsAPI.endSession(activeSession);
      toast.success("Session ended successfully.");
      refreshSessions?.();
      navigate("/dashboard");
    } catch {
      toast.error("Could not end session");
    }
  };

  const isCompleted = sessionDetails?.status === "completed";
  const shouldShowEndButton =
    activeSession && (sessionDetails?.status === "active" || !sessionDetails);

  return (
    <div className="flex flex-col h-screen">
      {/* Chat header */}
      <div className="px-6 py-4 bg-white border-b border-slate-100 flex items-center gap-3">
        <div className="w-9 h-9 rounded-xl bg-mint-100 flex items-center justify-center">
          <Bot size={18} className="text-mint-600" />
        </div>
        <div>
          <p className="font-display font-semibold text-slate-800 text-sm">
            MediSense AI
          </p>
          <div className="flex items-center gap-1.5">
            <span className="w-1.5 h-1.5 rounded-full bg-mint-500 animate-pulse-soft" />
            <span className="text-xs text-slate-400 font-body">
              Online — ready to help
            </span>
          </div>
        </div>
        <div className="ml-auto flex items-center gap-3">
          {shouldShowEndButton && (
            <button
              onClick={handleEndSession}
              className="px-3 py-1.5 bg-rose-50 hover:bg-rose-100 text-rose-600 rounded-lg text-xs font-display font-semibold transition-colors"
            >
              End Session
            </button>
          )}
        </div>
      </div>

      {/* Messages area */}
      <div
        ref={messagesContainerRef}
        className="flex-1 overflow-y-auto scrollbar-thin px-6 py-4"
      >
        {loadingMessages ? (
          <div className="flex justify-center items-center h-full">
            <Spinner />
          </div>
        ) : messages.length === 0 ? (
          <EmptyChat />
        ) : (
          <div className="flex flex-col gap-4 max-w-3xl mx-auto">
            {messages.map((msg) => (
              <Message key={msg.id} msg={msg} />
            ))}
            {sending && <TypingIndicator />}
            <div ref={bottomRef} />
          </div>
        )}
      </div>

      {/* Disclaimer */}
      <div className="px-6 py-2 text-center">
        <p className="text-xs text-slate-400 font-body">
          ⚕️ MediSense AI is for informational purposes only. Always consult a
          qualified doctor.
        </p>
      </div>

      {/* Input area */}
      {isCompleted ? (
        <div className="px-6 py-4 bg-slate-50 border-t border-slate-100 text-center">
          <p className="text-sm text-slate-500 font-body">
            This session has been completed and is read-only.
          </p>
        </div>
      ) : (
        <div className="px-6 pb-6 pt-3 bg-white border-t border-slate-100">
          <div className="max-w-3xl mx-auto flex items-end gap-3">
            <div className="flex-1 relative">
              <textarea
                id="chat-input"
                ref={inputRef}
                rows={1}
                value={input}
                onChange={(e) => {
                  setInput(e.target.value);
                  // auto-resize
                  e.target.style.height = "auto";
                  e.target.style.height =
                    Math.min(e.target.scrollHeight, 120) + "px";
                }}
                onInput={(e) => {
                  setInput(e.target.value);
                }}
                onKeyDown={handleKeyDown}
                placeholder="Describe your symptoms... (e.g. I have fever and body aches)"
                className="input-base resize-none py-3 pr-4 leading-relaxed scrollbar-thin"
                style={{ minHeight: "48px", maxHeight: "120px" }}
                disabled={sending}
              />
            </div>
            <button
              onClick={handleSend}
              disabled={!input.trim() || sending}
              className="w-12 h-12 rounded-xl bg-mint-500 hover:bg-mint-600 active:bg-mint-700
                text-white flex items-center justify-center flex-shrink-0
                shadow-mint transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {sending ? (
                <Spinner size={18} color="white" />
              ) : (
                <Send size={18} />
              )}
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
