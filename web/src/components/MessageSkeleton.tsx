export const MessageSkeleton = () => {
  return (
    <div className="space-y-6 px-4 py-6 sm:px-6 lg:px-8 animate-pulse">
      {/* AI Message Skeleton */}
      <div className="flex gap-4 items-start">
        <div className="flex-shrink-0 w-10 h-10 bg-muted rounded-full" />
        <div className="flex-1 max-w-[90%] space-y-2">
          <div className="h-4 bg-muted rounded w-3/4" />
          <div className="h-4 bg-muted rounded w-full" />
          <div className="h-4 bg-muted rounded w-5/6" />
        </div>
        <div className="flex-shrink-0 w-10 h-10" />
      </div>

      {/* User Message Skeleton */}
      <div className="flex gap-4 items-start">
        <div className="flex-shrink-0 w-10 h-10" />
        <div className="flex-1 flex justify-end">
          <div className="max-w-[85%] sm:max-w-[80%] md:max-w-[75%] space-y-2">
            <div className="h-4 bg-muted rounded w-full" />
            <div className="h-4 bg-muted rounded w-2/3" />
          </div>
        </div>
        <div className="flex-shrink-0 w-10 h-10 bg-muted rounded-full" />
      </div>

      {/* AI Message Skeleton */}
      <div className="flex gap-4 items-start">
        <div className="flex-shrink-0 w-10 h-10 bg-muted rounded-full" />
        <div className="flex-1 max-w-[90%] space-y-2">
          <div className="h-4 bg-muted rounded w-2/3" />
          <div className="h-4 bg-muted rounded w-full" />
          <div className="h-4 bg-muted rounded w-4/5" />
          <div className="h-4 bg-muted rounded w-3/4" />
        </div>
        <div className="flex-shrink-0 w-10 h-10" />
      </div>
    </div>
  );
};
