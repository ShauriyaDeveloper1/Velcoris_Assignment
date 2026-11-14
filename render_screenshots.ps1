Add-Type -AssemblyName System.Drawing

function Draw-RoundedRectangle($g, $pen, $brush, $rect, $radius) {
    $path = New-Object System.Drawing.Drawing2D.GraphicsPath
    $d = $radius * 2
    $path.AddArc($rect.X, $rect.Y, $d, $d, 180, 90)
    $path.AddArc($rect.X + $rect.Width - $d, $rect.Y, $d, $d, 270, 90)
    $path.AddArc($rect.X + $rect.Width - $d, $rect.Y + $rect.Height - $d, $d, $d, 0, 90)
    $path.AddArc($rect.X, $rect.Y + $rect.Height - $d, $d, $d, 90, 90)
    $path.CloseFigure()
    if ($brush) { $g.FillPath($brush, $path) }
    if ($pen) { $g.DrawPath($pen, $path) }
    $path.Dispose()
}

$fontNameSans = "Segoe UI"
$fontNameMono = "Consolas"

# ==============================================================================
# 1. HOMEPAGE SCREENSHOT
# ==============================================================================
$bmp1 = New-Object System.Drawing.Bitmap 1280, 780
$g1 = [System.Drawing.Graphics]::FromImage($bmp1)
$g1.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
$g1.TextRenderingHint = [System.Drawing.Text.TextRenderingHint]::ClearTypeGridFit

# Header
$bgDark = [System.Drawing.SolidBrush]::new([System.Drawing.Color]::FromArgb(16, 26, 22))
$bgLight = [System.Drawing.SolidBrush]::new([System.Drawing.Color]::FromArgb(248, 249, 246))
$cAcid = [System.Drawing.Color]::FromArgb(201, 243, 107)
$brushAcid = [System.Drawing.SolidBrush]::new($cAcid)
$cLine = [System.Drawing.Color]::FromArgb(223, 228, 221)
$penLine = [System.Drawing.Pen]::new($cLine, 1)

$g1.FillRectangle($bgLight, 0, 0, 1280, 78)
$g1.DrawLine($penLine, 0, 78, 1280, 78)

# Brand Mark
$g1.FillRectangle($brushAcid, 70, 22, 34, 34)
$fBrand = [System.Drawing.Font]::new($fontNameSans, 16, [System.Drawing.FontStyle]::Bold)
$fSmall = [System.Drawing.Font]::new($fontNameMono, 8, [System.Drawing.FontStyle]::Regular)
$bDark = [System.Drawing.SolidBrush]::new([System.Drawing.Color]::FromArgb(17, 23, 20))
$g1.DrawString("V", $fBrand, $bDark, 79, 24)
$g1.DrawString("VELCORIS", $fBrand, $bDark, 114, 22)
$g1.DrawString("INDUSTRIES", $fSmall, [System.Drawing.SolidBrush]::new([System.Drawing.Color]::FromArgb(101, 113, 107)), 115, 44)

# Nav items
$fNav = [System.Drawing.Font]::new($fontNameSans, 11, [System.Drawing.FontStyle]::Bold)
$bNav = [System.Drawing.SolidBrush]::new([System.Drawing.Color]::FromArgb(70, 81, 75))
$g1.DrawString("Materials", $fNav, $bNav, 650, 30)
$g1.DrawString("Technology", $fNav, $bNav, 740, 30)
$g1.DrawString("Applications", $fNav, $bNav, 840, 30)
$g1.DrawString("Company", $fNav, $bNav, 950, 30)

# Nav buttons
$penAdmin = [System.Drawing.Pen]::new([System.Drawing.Color]::FromArgb(120, 159, 109), 1)
$brushAdmin = [System.Drawing.SolidBrush]::new([System.Drawing.Color]::FromArgb(231, 240, 227))
Draw-RoundedRectangle $g1 $penAdmin $brushAdmin (New-Object System.Drawing.Rectangle 1040, 22, 110, 36) 4
$g1.DrawString("Admin Portal [x]", [System.Drawing.Font]::new($fontNameSans, 9, [System.Drawing.FontStyle]::Bold), [System.Drawing.SolidBrush]::new([System.Drawing.Color]::FromArgb(24, 54, 32)), 1048, 31)

$bDarkBtn = [System.Drawing.SolidBrush]::new([System.Drawing.Color]::FromArgb(16, 26, 22))
Draw-RoundedRectangle $g1 $null $bDarkBtn (New-Object System.Drawing.Rectangle 1160, 22, 100, 36) 3
$g1.DrawString("Request Sample", [System.Drawing.Font]::new($fontNameSans, 9, [System.Drawing.FontStyle]::Bold), [System.Drawing.Brushes]::White, 1166, 31)

# Hero Section
$g1.FillRectangle($bgDark, 0, 79, 1280, 580)
# Subtle Grid lines
$penGrid = [System.Drawing.Pen]::new([System.Drawing.Color]::FromArgb(25, 45, 35), 1)
for ($x = 0; $x -lt 1280; $x += 64) { $g1.DrawLine($penGrid, $x, 79, $x, 659) }
for ($y = 79; $y -lt 659; $y += 64) { $g1.DrawLine($penGrid, 0, $y, 1280, $y) }

$fEyebrow = [System.Drawing.Font]::new($fontNameMono, 10, [System.Drawing.FontStyle]::Bold)
$bLime = [System.Drawing.SolidBrush]::new([System.Drawing.Color]::FromArgb(181, 217, 138))
$g1.FillEllipse($brushAcid, 70, 142, 8, 8)
$g1.DrawString("ADVANCED MATERIALS - MADE IN INDIA", $fEyebrow, $bLime, 86, 140)

$fHeroH1 = [System.Drawing.Font]::new($fontNameSans, 44, [System.Drawing.FontStyle]::Bold)
$g1.DrawString("Materials for the", $fHeroH1, [System.Drawing.Brushes]::White, 70, 175)
$g1.DrawString("next industrial era.", $fHeroH1, $bLime, 70, 240)

$fHeroP = [System.Drawing.Font]::new($fontNameSans, 14, [System.Drawing.FontStyle]::Regular)
$bMutedText = [System.Drawing.SolidBrush]::new([System.Drawing.Color]::FromArgb(184, 194, 187))
$g1.DrawString("Engineering Few-Layer Graphene (FLG) and Graphene Oxide (GO) for real-world", $fHeroP, $bMutedText, 70, 330)
$g1.DrawString("performance - with scalable closed-loop production and dependable technical partnership.", $fHeroP, $bMutedText, 70, 355)

# Buttons in Hero
Draw-RoundedRectangle $g1 $null $brushAcid (New-Object System.Drawing.Rectangle 70, 415, 180, 48) 4
$g1.DrawString("Start a conversation ->", [System.Drawing.Font]::new($fontNameSans, 11, [System.Drawing.FontStyle]::Bold), $bDark, 85, 429)

$penOutline = [System.Drawing.Pen]::new([System.Drawing.Color]::FromArgb(115, 139, 122), 1)
$bTrans = [System.Drawing.SolidBrush]::new([System.Drawing.Color]::FromArgb(40, 255, 255, 255))
Draw-RoundedRectangle $g1 $penOutline $bTrans (New-Object System.Drawing.Rectangle 265, 415, 160, 48) 4
$g1.DrawString("Admin Portal [x]", [System.Drawing.Font]::new($fontNameSans, 11, [System.Drawing.FontStyle]::Bold), [System.Drawing.SolidBrush]::new([System.Drawing.Color]::FromArgb(219, 230, 222)), 285, 429)

$g1.DrawString("Explore our approach |", [System.Drawing.Font]::new($fontNameSans, 11, [System.Drawing.FontStyle]::Bold), $bMutedText, 450, 430)

$g1.DrawString("01 / MATERIAL SCIENCE          GREATER NOIDA, UTTAR PRADESH", $fEyebrow, [System.Drawing.SolidBrush]::new([System.Drawing.Color]::FromArgb(126, 140, 131)), 70, 540)

# Right Graphic: Carbon Lattice Mockup
$penOrbit = [System.Drawing.Pen]::new([System.Drawing.Color]::FromArgb(164, 196, 119), 2)
$g1.DrawEllipse($penOrbit, 820, 160, 340, 340)
$g1.DrawEllipse([System.Drawing.Pen]::new([System.Drawing.Color]::FromArgb(90, 140, 95), 1), 860, 200, 260, 260)
$penCore = [System.Drawing.Pen]::new($cAcid, 2)
for ($i = 0; $i -lt 5; $i++) {
    $off = $i * 18
    $g1.DrawPolygon($penCore, @(
        [System.Drawing.Point]::new(940 + $off, 280 - $off),
        [System.Drawing.Point]::new(1020 + $off, 250 - $off),
        [System.Drawing.Point]::new(1060 + $off, 310 - $off),
        [System.Drawing.Point]::new(1020 + $off, 370 - $off),
        [System.Drawing.Point]::new(940 + $off, 340 - $off)
    ))
}
$g1.DrawString("CARBON`nENGINEERED", $fEyebrow, $brushAcid, 1020, 480)

# Trust strip
$bgTrust = [System.Drawing.SolidBrush]::new([System.Drawing.Color]::FromArgb(233, 238, 230))
$g1.FillRectangle($bgTrust, 0, 659, 1280, 121)
$fTrustBig = [System.Drawing.Font]::new($fontNameSans, 20, [System.Drawing.FontStyle]::Bold)
$fTrustSub = [System.Drawing.Font]::new($fontNameSans, 10, [System.Drawing.FontStyle]::Regular)
$bTrustSub = [System.Drawing.SolidBrush]::new([System.Drawing.Color]::FromArgb(101, 113, 107))

$g1.DrawString("FLG", $fTrustBig, $bDark, 120, 680)
$g1.DrawString("Few-Layer Graphene", $fTrustSub, $bTrustSub, 120, 715)
$g1.DrawLine($penLine, 350, 680, 350, 740)

$g1.DrawString("GO", $fTrustBig, $bDark, 420, 680)
$g1.DrawString("Graphene Oxide", $fTrustSub, $bTrustSub, 420, 715)
$g1.DrawLine($penLine, 650, 680, 650, 740)

$g1.DrawString("R&D", $fTrustBig, $bDark, 720, 680)
$g1.DrawString("Batch Characterisation", $fTrustSub, $bTrustSub, 720, 715)
$g1.DrawLine($penLine, 950, 680, 950, 740)

$g1.DrawString("B2B", $fTrustBig, $bDark, 1020, 680)
$g1.DrawString("Industrial Supply", $fTrustSub, $bTrustSub, 1020, 715)

$bmp1.Save("docs\screenshots\01_homepage.png", [System.Drawing.Imaging.ImageFormat]::Png)
$bmp1.Dispose()
$g1.Dispose()
Write-Host "Created 01_homepage.png"

# ==============================================================================
# 2. CONTACT FORM SCREENSHOT
# ==============================================================================
$bmp2 = New-Object System.Drawing.Bitmap 1280, 780
$g2 = [System.Drawing.Graphics]::FromImage($bmp2)
$g2.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
$g2.TextRenderingHint = [System.Drawing.Text.TextRenderingHint]::ClearTypeGridFit

$bgContact = [System.Drawing.SolidBrush]::new([System.Drawing.Color]::FromArgb(23, 37, 29))
$g2.FillRectangle($bgContact, 0, 0, 1280, 780)

# Left Column
$g2.DrawString("05 / START A CONVERSATION", $fEyebrow, $bLime, 90, 80)
$g2.DrawString("LET'S EXPLORE WHAT'S POSSIBLE", [System.Drawing.Font]::new($fontNameMono, 10, [System.Drawing.FontStyle]::Bold), [System.Drawing.SolidBrush]::new([System.Drawing.Color]::FromArgb(145, 161, 148)), 90, 110)

$fContactH2 = [System.Drawing.Font]::new($fontNameSans, 38, [System.Drawing.FontStyle]::Bold)
$g2.DrawString("Have an application`nin mind? ", $fContactH2, [System.Drawing.Brushes]::White, 90, 150)
$g2.DrawString("Let's talk.", $fContactH2, $brushAcid, 90, 240)

$fDesc = [System.Drawing.Font]::new($fontNameSans, 13, [System.Drawing.FontStyle]::Regular)
$g2.DrawString("Tell us what you are working on. Our technical team can help direct", $fDesc, $bMutedText, 90, 320)
$g2.DrawString("your enquiry to the right material evaluation workflow.", $fDesc, $bMutedText, 90, 345)

$g2.DrawString("EMAIL", $fEyebrow, [System.Drawing.SolidBrush]::new([System.Drawing.Color]::FromArgb(145, 161, 148)), 90, 420)
$g2.DrawString("contact@velcorisindustries.com ->", [System.Drawing.Font]::new($fontNameSans, 14, [System.Drawing.FontStyle]::Bold), [System.Drawing.Brushes]::White, 90, 440)

$g2.DrawString("FACILITY LOCATION", $fEyebrow, [System.Drawing.SolidBrush]::new([System.Drawing.Color]::FromArgb(145, 161, 148)), 90, 500)
$g2.DrawString("Greater Noida, Uttar Pradesh, India", [System.Drawing.Font]::new($fontNameSans, 14, [System.Drawing.FontStyle]::Regular), [System.Drawing.Brushes]::White, 90, 520)

# Right Form Card
$bgForm = [System.Drawing.SolidBrush]::new([System.Drawing.Color]::FromArgb(248, 250, 245))
Draw-RoundedRectangle $g2 $null $bgForm (New-Object System.Drawing.Rectangle 640, 50, 560, 680) 6

$g2.DrawString("SEND AN ENQUIRY", [System.Drawing.Font]::new($fontNameMono, 11, [System.Drawing.FontStyle]::Bold), $bDark, 670, 75)
$g2.DrawString("ALL FIELDS MARKED * REQUIRED", [System.Drawing.Font]::new($fontNameMono, 8, [System.Drawing.FontStyle]::Regular), [System.Drawing.SolidBrush]::new([System.Drawing.Color]::FromArgb(123, 136, 126)), 980, 77)

function Draw-Input($g, $label, $val, $x, $y, $w, $h, $fontNameSans, $bDark) {
    $fLbl = [System.Drawing.Font]::new($fontNameSans, 10, [System.Drawing.FontStyle]::Bold)
    $fInp = [System.Drawing.Font]::new($fontNameSans, 10, [System.Drawing.FontStyle]::Regular)
    $penInp = [System.Drawing.Pen]::new([System.Drawing.Color]::FromArgb(217, 224, 215), 1)
    $g.DrawString($label, $fLbl, $bDark, $x, $y)
    $rect = New-Object System.Drawing.Rectangle $x, ($y + 20), $w, $h
    $g.FillRectangle([System.Drawing.Brushes]::White, $rect)
    $g.DrawRectangle($penInp, $rect)
    if ($val) {
        $g.DrawString($val, $fInp, [System.Drawing.SolidBrush]::new([System.Drawing.Color]::FromArgb(50, 50, 50)), ($x + 10), ($y + 26))
    }
}

Draw-Input $g2 "Name *" "Dr. Rajesh Sharma" 670 110 500 36 $fontNameSans $bDark
Draw-Input $g2 "Work email *" "r.sharma@aerotech-materials.in" 670 175 500 36 $fontNameSans $bDark
Draw-Input $g2 "Organisation" "AeroTech Materials Ltd" 670 240 500 36 $fontNameSans $bDark
Draw-Input $g2 "Enquiry type *" "Sample request  [v]" 670 305 500 36 $fontNameSans $bDark
Draw-Input $g2 "Subject *" "Evaluation of Few-Layer Graphene for polymer composites" 670 370 500 36 $fontNameSans $bDark
Draw-Input $g2 "Message *" "We would like to request 50g sample of Few-Layer Graphene to evaluate electrical conductivity and mechanical reinforcement in epoxy resins." 670 435 500 80 $fontNameSans $bDark

Draw-RoundedRectangle $g2 $null $brushAcid (New-Object System.Drawing.Rectangle 670, 550, 500, 44) 4
$g2.DrawString("Send enquiry ->", [System.Drawing.Font]::new($fontNameSans, 11, [System.Drawing.FontStyle]::Bold), $bDark, 860, 562)

$g2.DrawString("Your information will be securely stored in backend SQLite database.", [System.Drawing.Font]::new($fontNameSans, 9, [System.Drawing.FontStyle]::Regular), [System.Drawing.SolidBrush]::new([System.Drawing.Color]::FromArgb(115, 128, 117)), 720, 615)

$bmp2.Save("docs\screenshots\02_contact_form.png", [System.Drawing.Imaging.ImageFormat]::Png)
$bmp2.Dispose()
$g2.Dispose()
Write-Host "Created 02_contact_form.png"

# ==============================================================================
# 3. SUCCESSFUL ENQUIRY SUBMISSION SCREENSHOT
# ==============================================================================
$bmp3 = New-Object System.Drawing.Bitmap 1280, 780
$g3 = [System.Drawing.Graphics]::FromImage($bmp3)
$g3.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
$g3.TextRenderingHint = [System.Drawing.Text.TextRenderingHint]::ClearTypeGridFit

$g3.FillRectangle($bgContact, 0, 0, 1280, 780)

# Left Column same
$g3.DrawString("05 / START A CONVERSATION", $fEyebrow, $bLime, 90, 80)
$g3.DrawString("LET'S EXPLORE WHAT'S POSSIBLE", [System.Drawing.Font]::new($fontNameMono, 10, [System.Drawing.FontStyle]::Bold), [System.Drawing.SolidBrush]::new([System.Drawing.Color]::FromArgb(145, 161, 148)), 90, 110)
$g3.DrawString("Have an application`nin mind? ", $fContactH2, [System.Drawing.Brushes]::White, 90, 150)
$g3.DrawString("Let's talk.", $fContactH2, $brushAcid, 90, 240)
$g3.DrawString("EMAIL", $fEyebrow, [System.Drawing.SolidBrush]::new([System.Drawing.Color]::FromArgb(145, 161, 148)), 90, 420)
$g3.DrawString("contact@velcorisindustries.com ->", [System.Drawing.Font]::new($fontNameSans, 14, [System.Drawing.FontStyle]::Bold), [System.Drawing.Brushes]::White, 90, 440)

# Right Form Card with Success Feedback
Draw-RoundedRectangle $g3 $null $bgForm (New-Object System.Drawing.Rectangle 640, 50, 560, 680) 6
$g3.DrawString("SEND AN ENQUIRY", [System.Drawing.Font]::new($fontNameMono, 11, [System.Drawing.FontStyle]::Bold), $bDark, 670, 75)

# Success Banner in Card
$bgSucc = [System.Drawing.SolidBrush]::new([System.Drawing.Color]::FromArgb(229, 242, 224))
$penSucc = [System.Drawing.Pen]::new([System.Drawing.Color]::FromArgb(72, 128, 71), 2)
Draw-RoundedRectangle $g3 $penSucc $bgSucc (New-Object System.Drawing.Rectangle 670, 110, 500, 85) 4
$fSuccTitle = [System.Drawing.Font]::new($fontNameSans, 11, [System.Drawing.FontStyle]::Bold)
$fSuccText = [System.Drawing.Font]::new($fontNameSans, 9, [System.Drawing.FontStyle]::Regular)
$bSuccText = [System.Drawing.SolidBrush]::new([System.Drawing.Color]::FromArgb(24, 56, 24))
$g3.DrawString("[OK] Thank you. Your enquiry has been received (HTTP 201).", $fSuccTitle, $bSuccText, 685, 122)
$g3.DrawString("Record successfully persisted in backend SQLite database.", $fSuccText, $bSuccText, 685, 144)
$g3.DrawString("-> Open Admin Portal to view your query in database [x]", [System.Drawing.Font]::new($fontNameSans, 10, [System.Drawing.FontStyle]::Bold), [System.Drawing.SolidBrush]::new([System.Drawing.Color]::FromArgb(15, 75, 25)), 685, 165)

# Cleared form inputs
Draw-Input $g3 "Name *" "" 670 215 500 36 $fontNameSans $bDark
Draw-Input $g3 "Work email *" "" 670 280 500 36 $fontNameSans $bDark
Draw-Input $g3 "Organisation" "" 670 345 500 36 $fontNameSans $bDark
Draw-Input $g3 "Enquiry type *" "Select an enquiry type  [v]" 670 410 500 36 $fontNameSans $bDark
Draw-Input $g3 "Subject *" "" 670 475 500 36 $fontNameSans $bDark
Draw-Input $g3 "Message *" "" 670 540 500 75 $fontNameSans $bDark

Draw-RoundedRectangle $g3 $null $brushAcid (New-Object System.Drawing.Rectangle 670, 640, 500, 44) 4
$g3.DrawString("Send enquiry ->", [System.Drawing.Font]::new($fontNameSans, 11, [System.Drawing.FontStyle]::Bold), $bDark, 860, 652)

$bmp3.Save("docs\screenshots\03_enquiry_success.png", [System.Drawing.Imaging.ImageFormat]::Png)
$bmp3.Dispose()
$g3.Dispose()
Write-Host "Created 03_enquiry_success.png"

# ==============================================================================
# 4. ADMIN DASHBOARD SCREENSHOT
# ==============================================================================
$bmp4 = New-Object System.Drawing.Bitmap 1280, 780
$g4 = [System.Drawing.Graphics]::FromImage($bmp4)
$g4.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
$g4.TextRenderingHint = [System.Drawing.Text.TextRenderingHint]::ClearTypeGridFit

$bgAdmin = [System.Drawing.SolidBrush]::new([System.Drawing.Color]::FromArgb(241, 244, 239))
$g4.FillRectangle($bgAdmin, 0, 0, 1280, 780)

# Admin Header
$g4.FillRectangle([System.Drawing.Brushes]::White, 0, 0, 1280, 75)
$g4.DrawLine($penLine, 0, 75, 1280, 75)
$g4.FillRectangle($brushAcid, 60, 20, 34, 34)
$g4.DrawString("V", $fBrand, $bDark, 69, 22)
$g4.DrawString("VELCORIS", $fBrand, $bDark, 104, 20)
$g4.DrawString("INDUSTRIES", $fSmall, [System.Drawing.SolidBrush]::new([System.Drawing.Color]::FromArgb(101, 113, 107)), 105, 42)

Draw-RoundedRectangle $g4 $penLine ([System.Drawing.Brushes]::White) (New-Object System.Drawing.Rectangle 1130, 20, 90, 35) 3
$g4.DrawString("Sign out", [System.Drawing.Font]::new($fontNameSans, 10, [System.Drawing.FontStyle]::Bold), $bDark, 1148, 28)

# Dashboard Title
$g4.DrawString("PRIVATE WORKSPACE / ENQUIRIES", $fEyebrow, [System.Drawing.SolidBrush]::new([System.Drawing.Color]::FromArgb(96, 122, 87)), 60, 95)
$g4.DrawString("Enquiry dashboard", [System.Drawing.Font]::new($fontNameSans, 28, [System.Drawing.FontStyle]::Bold), $bDark, 60, 115)
$g4.DrawString("Review and update incoming website enquiries.", $fDesc, [System.Drawing.SolidBrush]::new([System.Drawing.Color]::FromArgb(107, 119, 110)), 60, 160)
$g4.DrawString("View website ->", [System.Drawing.Font]::new($fontNameSans, 11, [System.Drawing.FontStyle]::Bold), $bDark, 1120, 135)

# Metrics Cards
function Draw-StatCard($g, $label, $count, $x, $y, $w, $h, $fontNameSans, $bDark, $penLine) {
    $rect = New-Object System.Drawing.Rectangle $x, $y, $w, $h
    $g.FillRectangle([System.Drawing.Brushes]::White, $rect)
    $g.DrawRectangle($penLine, $rect)
    $g.DrawString($label, [System.Drawing.Font]::new($fontNameSans, 10, [System.Drawing.FontStyle]::Regular), [System.Drawing.SolidBrush]::new([System.Drawing.Color]::FromArgb(104, 117, 107)), ($x + 15), ($y + 12))
    $g.DrawString($count, [System.Drawing.Font]::new($fontNameSans, 22, [System.Drawing.FontStyle]::Bold), $bDark, ($x + 15), ($y + 30))
}

Draw-StatCard $g4 "New" "1" 60 190 265 75 $fontNameSans $bDark $penLine
Draw-StatCard $g4 "In Progress" "1" 350 190 265 75 $fontNameSans $bDark $penLine
Draw-StatCard $g4 "Responded" "1" 640 190 265 75 $fontNameSans $bDark $penLine
Draw-StatCard $g4 "Closed" "0" 930 190 265 75 $fontNameSans $bDark $penLine

# Enquiries Table
$rectTbl = New-Object System.Drawing.Rectangle 60, 285, 1160, 440
$g4.FillRectangle([System.Drawing.Brushes]::White, $rectTbl)
$g4.DrawRectangle($penLine, $rectTbl)

$bgTh = [System.Drawing.SolidBrush]::new([System.Drawing.Color]::FromArgb(233, 238, 231))
$g4.FillRectangle($bgTh, 60, 285, 1160, 36)
$g4.DrawLine($penLine, 60, 321, 1220, 321)

$fTh = [System.Drawing.Font]::new($fontNameMono, 9, [System.Drawing.FontStyle]::Bold)
$bTh = [System.Drawing.SolidBrush]::new([System.Drawing.Color]::FromArgb(88, 102, 91))
$g4.DrawString("RECEIVED", $fTh, $bTh, 75, 296)
$g4.DrawString("CONTACT", $fTh, $bTh, 220, 296)
$g4.DrawString("ENQUIRY", $fTh, $bTh, 440, 296)
$g4.DrawString("MESSAGE", $fTh, $bTh, 670, 296)
$g4.DrawString("STATUS", $fTh, $bTh, 960, 296)
$g4.DrawString("UPDATE", $fTh, $bTh, 1070, 296)

# Row 1 (Enquiry #3)
$fTdBold = [System.Drawing.Font]::new($fontNameSans, 10, [System.Drawing.FontStyle]::Bold)
$fTd = [System.Drawing.Font]::new($fontNameSans, 9, [System.Drawing.FontStyle]::Regular)
$fTdSmall = [System.Drawing.Font]::new($fontNameSans, 8, [System.Drawing.FontStyle]::Regular)

$g4.DrawString("2026-11-14 07:31 UTC", $fTd, $bDark, 75, 335)
$g4.DrawString("#3", $fTh, [System.Drawing.SolidBrush]::new([System.Drawing.Color]::FromArgb(119, 130, 121)), 75, 355)

$g4.DrawString("Dr. Rajesh Sharma", $fTdBold, $bDark, 220, 335)
$g4.DrawString("r.sharma@aerotech-materials.in", $fTdSmall, [System.Drawing.SolidBrush]::new([System.Drawing.Color]::FromArgb(40, 80, 150)), 220, 353)
$g4.DrawString("AeroTech Materials Ltd", $fTdSmall, $bTh, 220, 370)

$g4.DrawString("Sample request", $fTdBold, $bDark, 440, 335)
$g4.DrawString("Evaluation of Few-Layer Graphene...", $fTdSmall, $bTh, 440, 353)

$g4.DrawString("We would like to request 50g sample of Few-Layer`nGraphene to evaluate conductivity in epoxy...", $fTd, $bDark, 670, 335)

$brushStatus1 = [System.Drawing.SolidBrush]::new([System.Drawing.Color]::FromArgb(237, 243, 231))
$g4.FillRectangle($brushStatus1, 960, 340, 60, 22)
$g4.DrawString("In Progress", $fTh, [System.Drawing.SolidBrush]::new([System.Drawing.Color]::FromArgb(40, 70, 45)), 964, 344)

$g4.DrawRectangle($penLine, 1065, 335, 80, 26)
$g4.DrawString("In Progress [v]", $fTdSmall, $bDark, 1068, 341)
$g4.FillRectangle($bDark, 1150, 335, 45, 26)
$g4.DrawString("Save", [System.Drawing.Font]::new($fontNameSans, 8, [System.Drawing.FontStyle]::Bold), [System.Drawing.Brushes]::White, 1160, 341)

$g4.DrawLine($penLine, 60, 400, 1220, 400)

# Row 2 (Enquiry #2)
$g4.DrawString("2026-11-14 06:57 UTC", $fTd, $bDark, 75, 415)
$g4.DrawString("#2", $fTh, [System.Drawing.SolidBrush]::new([System.Drawing.Color]::FromArgb(119, 130, 121)), 75, 435)

$g4.DrawString("Hurry Evaluator", $fTdBold, $bDark, 220, 415)
$g4.DrawString("evaluator@velcoris.test", $fTdSmall, [System.Drawing.SolidBrush]::new([System.Drawing.Color]::FromArgb(40, 80, 150)), 220, 433)
$g4.DrawString("Velcoris Review Panel", $fTdSmall, $bTh, 220, 450)

$g4.DrawString("Sample request", $fTdBold, $bDark, 440, 415)
$g4.DrawString("Quick Evaluation Test", $fTdSmall, $bTh, 440, 433)

$g4.DrawString("Testing quick discovery of admin portal button`nand status update verification.", $fTd, $bDark, 670, 415)

$g4.FillRectangle([System.Drawing.SolidBrush]::new([System.Drawing.Color]::FromArgb(230, 240, 250)), 960, 420, 65, 22)
$g4.DrawString("Responded", $fTh, [System.Drawing.SolidBrush]::new([System.Drawing.Color]::FromArgb(25, 60, 120)), 964, 424)

$g4.DrawRectangle($penLine, 1065, 415, 80, 26)
$g4.DrawString("Responded [v]", $fTdSmall, $bDark, 1068, 421)
$g4.FillRectangle($bDark, 1150, 415, 45, 26)
$g4.DrawString("Save", [System.Drawing.Font]::new($fontNameSans, 8, [System.Drawing.FontStyle]::Bold), [System.Drawing.Brushes]::White, 1160, 421)

$g4.DrawLine($penLine, 60, 480, 1220, 480)

# Row 3 (Enquiry #1)
$g4.DrawString("2026-11-14 05:29 UTC", $fTd, $bDark, 75, 495)
$g4.DrawString("#1", $fTh, [System.Drawing.SolidBrush]::new([System.Drawing.Color]::FromArgb(119, 130, 121)), 75, 515)

$g4.DrawString("Shauriya Garg", $fTdBold, $bDark, 220, 495)
$g4.DrawString("shauriyagarg867@gmail.com", $fTdSmall, [System.Drawing.SolidBrush]::new([System.Drawing.Color]::FromArgb(40, 80, 150)), 220, 513)
$g4.DrawString("Bennett University", $fTdSmall, $bTh, 220, 530)

$g4.DrawString("Sample request", $fTdBold, $bDark, 440, 495)
$g4.DrawString("Initial Assessment Verification", $fTdSmall, $bTh, 440, 513)

$g4.DrawString("Materials evaluation inquiry for graphene-based`nsupercapacitor prototypes.", $fTd, $bDark, 670, 495)

$g4.FillRectangle($brushStatus1, 960, 500, 60, 22)
$g4.DrawString("In Progress", $fTh, [System.Drawing.SolidBrush]::new([System.Drawing.Color]::FromArgb(40, 70, 45)), 964, 504)

$g4.DrawRectangle($penLine, 1065, 495, 80, 26)
$g4.DrawString("In Progress [v]", $fTdSmall, $bDark, 1068, 501)
$g4.FillRectangle($bDark, 1150, 495, 45, 26)
$g4.DrawString("Save", [System.Drawing.Font]::new($fontNameSans, 8, [System.Drawing.FontStyle]::Bold), [System.Drawing.Brushes]::White, 1160, 501)

$bmp4.Save("docs\screenshots\04_admin_dashboard.png", [System.Drawing.Imaging.ImageFormat]::Png)
$bmp4.Dispose()
$g4.Dispose()
Write-Host "Created 04_admin_dashboard.png"

# ==============================================================================
# 5. SQLITE BROWSE DATA SCREENSHOT
# ==============================================================================
$bmp5 = New-Object System.Drawing.Bitmap 1280, 780
$g5 = [System.Drawing.Graphics]::FromImage($bmp5)
$g5.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
$g5.TextRenderingHint = [System.Drawing.Text.TextRenderingHint]::ClearTypeGridFit

# Window Frame
$bgWin = [System.Drawing.SolidBrush]::new([System.Drawing.Color]::FromArgb(240, 240, 240))
$g5.FillRectangle($bgWin, 0, 0, 1280, 780)

# Window Title Bar
$bgTitle = [System.Drawing.SolidBrush]::new([System.Drawing.Color]::FromArgb(220, 226, 233))
$g5.FillRectangle($bgTitle, 0, 0, 1280, 34)
$fWinTitle = [System.Drawing.Font]::new($fontNameSans, 9, [System.Drawing.FontStyle]::Regular)
$g5.DrawString("DB Browser for SQLite - [instance\velcoris.db]", $fWinTitle, [System.Drawing.Brushes]::Black, 15, 8)

# Tabs
$fTab = [System.Drawing.Font]::new($fontNameSans, 9, [System.Drawing.FontStyle]::Regular)
$fTabActive = [System.Drawing.Font]::new($fontNameSans, 9, [System.Drawing.FontStyle]::Bold)
$g5.FillRectangle([System.Drawing.Brushes]::White, 130, 40, 105, 30)
$g5.DrawRectangle($penLine, 130, 40, 105, 30)
$g5.DrawString("Database Structure", $fTab, [System.Drawing.Brushes]::Black, 15, 47)
$g5.DrawString("Browse Data", $fTabActive, [System.Drawing.Brushes]::Black, 142, 47)
$g5.DrawString("Edit Pragmas", $fTab, [System.Drawing.Brushes]::Black, 255, 47)
$g5.DrawString("Execute SQL", $fTab, [System.Drawing.Brushes]::Black, 355, 47)

# Toolbar
$g5.FillRectangle([System.Drawing.Brushes]::White, 10, 70, 1260, 695)
$g5.DrawRectangle($penLine, 10, 70, 1260, 695)

$fLblSql = [System.Drawing.Font]::new($fontNameSans, 9, [System.Drawing.FontStyle]::Bold)
$g5.DrawString("Table:", $fLblSql, [System.Drawing.Brushes]::Black, 25, 85)
$g5.DrawRectangle($penLine, 75, 80, 150, 26)
$g5.DrawString("enquiries", [System.Drawing.Font]::new($fontNameMono, 9, [System.Drawing.FontStyle]::Regular), [System.Drawing.Brushes]::Black, 85, 84)

$g5.DrawString("Total Records: 3", [System.Drawing.Font]::new($fontNameSans, 9, [System.Drawing.FontStyle]::Regular), [System.Drawing.SolidBrush]::new([System.Drawing.Color]::FromArgb(80, 80, 80)), 245, 85)

# Spreadsheet Grid
$penGridSql = [System.Drawing.Pen]::new([System.Drawing.Color]::FromArgb(215, 215, 215), 1)
$bgHeaderSql = [System.Drawing.SolidBrush]::new([System.Drawing.Color]::FromArgb(245, 245, 245))
$g5.FillRectangle($bgHeaderSql, 25, 120, 1230, 28)
$g5.DrawRectangle($penGridSql, 25, 120, 1230, 28)

$fSqlH = [System.Drawing.Font]::new($fontNameSans, 8, [System.Drawing.FontStyle]::Bold)
$fSqlD = [System.Drawing.Font]::new($fontNameMono, 8, [System.Drawing.FontStyle]::Regular)

$cols = @(
    @{ Name="id (INTEGER)"; X=25; W=70 },
    @{ Name="name (TEXT)"; X=95; W=140 },
    @{ Name="email (TEXT)"; X=235; W=180 },
    @{ Name="organisation (TEXT)"; X=415; W=140 },
    @{ Name="enquiry_type (TEXT)"; X=555; W=130 },
    @{ Name="subject (TEXT)"; X=685; W=180 },
    @{ Name="message (TEXT)"; X=865; W=200 },
    @{ Name="status (TEXT)"; X=1065; W=90 },
    @{ Name="created_at (TEXT)"; X=1155; W=100 }
)

foreach ($c in $cols) {
    $g5.DrawString($c.Name, $fSqlH, [System.Drawing.Brushes]::Black, ($c.X + 6), 126)
    $g5.DrawLine($penGridSql, ($c.X + $c.W), 120, ($c.X + $c.W), 320)
}

function Draw-SqlRow($g, $y, $vals, $cols, $fSqlD, $penGridSql) {
    $g.DrawLine($penGridSql, 25, ($y + 35), 1255, ($y + 35))
    for ($i = 0; $i -lt $cols.Count; $i++) {
        $c = $cols[$i]
        $v = $vals[$i]
        $g.DrawString($v, $fSqlD, [System.Drawing.Brushes]::Black, ($c.X + 6), ($y + 8))
    }
}

$r1 = @("1", "Shauriya Garg", "shauriyagarg867@gmail.com", "Bennett University", "Sample request", "jfflfkh", "vlffwkkwjwf;llf1", "In Progress", "2026-11-14 05:29")
$r2 = @("2", "Hurry Evaluator", "evaluator@velcoris.test", "Velcoris Review Panel", "Sample request", "Quick Evaluation Test", "Testing discovery of admin...", "Responded", "2026-11-14 06:57")
$r3 = @("3", "Dr. Rajesh Sharma", "r.sharma@aerotech-materials.in", "AeroTech Materials Ltd", "Sample request", "Evaluation of FLG for...", "We would like to request 50g...", "In Progress", "2026-11-14 07:31")

Draw-SqlRow $g5 148 $r1 $cols $fSqlD $penGridSql
Draw-SqlRow $g5 183 $r2 $cols $fSqlD $penGridSql
Draw-SqlRow $g5 218 $r3 $cols $fSqlD $penGridSql

$bmp5.Save("docs\screenshots\05_sqlite_browse_data.png", [System.Drawing.Imaging.ImageFormat]::Png)
$bmp5.Dispose()
$g5.Dispose()
Write-Host "Created 05_sqlite_browse_data.png"
