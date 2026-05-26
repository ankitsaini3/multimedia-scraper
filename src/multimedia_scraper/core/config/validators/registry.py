ALLOWED_FIELDS: frozenset[str] = frozenset({
    "logging.level",
    "logging.json_logs",
    "cache.enabled",
    "cache.root_directory",
    "cache.max_size_mb",
    "ffmpeg.executable_path",
    "ffmpeg.hwaccel_enabled",
    "ffmpeg.max_parallel_jobs",
})