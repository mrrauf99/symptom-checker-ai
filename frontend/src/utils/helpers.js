export function formatDate(dateStr) {
  if (!dateStr) return "";
  // Parse ISO string (with Z for UTC)
  let date = new Date(dateStr);

  // If no timezone indicator, add Z to ensure UTC parsing
  if (
    typeof dateStr === "string" &&
    !dateStr.includes("Z") &&
    !dateStr.includes("+") &&
    !dateStr.includes("-")
  ) {
    date = new Date(dateStr + "Z");
  }

  // Get timezone offset in minutes and convert to local time
  const offset = date.getTimezoneOffset();
  const localDate = new Date(date.getTime() - offset * 60 * 1000);

  return localDate.toLocaleDateString("en-US", {
    month: "short",
    day: "numeric",
    year: "numeric",
  });
}

export function formatTime(dateStr) {
  if (!dateStr) return "";

  // Parse ISO string (with Z for UTC)
  let date = new Date(dateStr);

  // If no timezone indicator, add Z to ensure UTC parsing
  if (
    typeof dateStr === "string" &&
    !dateStr.includes("Z") &&
    !dateStr.includes("+") &&
    !dateStr.includes("-")
  ) {
    date = new Date(dateStr + "Z");
  }

  // Get timezone offset in minutes and convert to local time
  const offset = date.getTimezoneOffset();
  const localDate = new Date(date.getTime() - offset * 60 * 1000);

  return localDate.toLocaleTimeString("en-US", {
    hour: "2-digit",
    minute: "2-digit",
    hour12: true,
  });
}

export function formatRelative(dateStr) {
  if (!dateStr) return "";
  const date = new Date(dateStr);
  const now = new Date();
  const diff = now - date;
  const mins = Math.floor(diff / 60000);
  const hours = Math.floor(diff / 3600000);
  const days = Math.floor(diff / 86400000);

  if (mins < 1) return "Just now";
  if (mins < 60) return `${mins}m ago`;
  if (hours < 24) return `${hours}h ago`;
  if (days === 1) return "Yesterday";
  return formatDate(dateStr);
}

export function getErrorMessage(error) {
  const detail = error?.response?.data?.detail;

  if (Array.isArray(detail)) {
    return detail.map((e) => e.msg).join(". ");
  }

  return (
    detail ||
    error?.response?.data?.message ||
    error?.message ||
    "Something went wrong. Please try again."
  );
}
