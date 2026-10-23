package se.korkort

/** Compose 1.9.3's browser bridge omits radio roles and pending checked state. */
internal expect fun updateBrowserAssessmentChoices(selectedLetter:String?,enabled:Boolean)
internal expect fun clearBrowserAssessmentChoices()
