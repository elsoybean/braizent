---
name: recipe-card
description: Creates a printable recipe card PDF from a recipe in the collection
---

# Recipe Card Generator

## Step 1: Get the Recipe Name
The user must provide a recipe name. If no name is provided, ask for it before proceeding.

You can also offer to list available recipes by searching the `./recipes/` directory if the user is unsure.

## Step 2: Find the Recipe File
Use the Glob tool to search for the recipe markdown file in `./recipes/`:
- Search for recipe folders: `recipes/*/[recipe-name].md`
- If the user provided an exact filename, use that
- Otherwise, search for files matching the recipe name pattern (e.g., `recipes/*chicken-congee*/*.md`)

If multiple matches are found, ask the user to clarify which recipe they want.
If no match is found, inform the user and offer to list available recipes.

Note: Each recipe lives in its own folder (e.g., `recipes/chicken-congee/chicken-congee.md`)

## Step 3: Read the Recipe
Use the Read tool to load the complete recipe markdown file.

## Step 3A: Check for Precise Variant

After reading the recipe, check if a `_precise` variant exists in the same folder:

Use Glob to search for: `recipes/[recipe-folder]/*_precise.md`

### If a Precise Variant Exists:

Ask the user which version they want to use for the recipe card:

"I found both the original recipe and a precise variant:
- **Original:** [recipe-name.md](recipes/folder/recipe-name.md)
- **Precise variant:** [recipe-name_precise.md](recipes/folder/recipe-name_precise.md)

Which would you like to use for the recipe card?"

If they choose the precise variant, use the Read tool to load that file instead and proceed with it.

### If No Precise Variant Exists:

Check if the recipe has flexible measurements or high-level instructions that might benefit from a precise variant.

**Indicators that a precise variant would be helpful:**
- Recipe has "Type: Quick Staple" header
- Ingredients use "to taste", "~", or lack specific quantities
- Instructions are high-level memory joggers rather than detailed steps
- Servings say "Flexible - adjust as needed"
- Times use "~" for approximation

**If the recipe lacks precision AND user might be sharing it:**

Inform the user and offer to create a precise variant:

"This recipe has flexible measurements and high-level instructions, which is great for personal use but might be unclear for others.

Would you like to:
1. **Create a precise variant first** - Work with me to add specific measurements and detailed instructions, then make the recipe card from that (recommended for sharing)
2. **Use the original as-is** - Make the recipe card from the flexible version (fine for personal use)
3. **Cancel** - Don't create a recipe card right now"

If they choose option 1:
- Inform them: "Let's use the `/recipe-variant` skill to create a precise variant first, then I'll make the recipe card from that."
- Use the Skill tool to invoke the recipe-variant skill with appropriate guidance
- After the variant is created, load it and continue with recipe card generation

If they choose option 2:
- Continue with the original recipe
- Note that the HTML/PDF formatting will adapt to handle flexible measurements

If they choose option 3:
- Stop and exit the skill

### If Recipe Already Has Precision:

If the recipe already has specific measurements and detailed instructions (standard imported recipe format), proceed directly to Step 4.

## Step 4: Generate the Recipe Card HTML
Create a beautifully formatted HTML file that presents the recipe in a printable format. The HTML should:

### 4.1 Layout Design
- Single-page layout optimized for printing or saving as PDF (must fit on one page)
- Compact design with minimal margins (0.2 inches)
- Two-column grid layout for ingredients to save space
- Clean, readable typography with proper hierarchy (10pt base font)
- Professional recipe card appearance
- Include all recipe information in an organized format

### 4.2 Content Sections
Include these sections from the recipe:
1. **Header**: Recipe title, cuisine, category (or type for quick staples)
2. **Metadata**: Servings, total time, active time (if available)
3. **Description**: The recipe description
4. **Ingredients**: Formatted appropriately based on recipe format:
   - **Standard recipes**: Use two-column grid with table format (quantity | unit | ingredient | prep)
   - **Quick staples**: Format ingredient lists or prose flexibly, preserving the memory-aid style
5. **Instructions**: Clear numbered steps (adapt formatting for high-level vs. detailed steps)
6. **Notes**: Both source notes and personal notes (if present)
7. **Footer**: Source attribution and URL (or note if it's a personal recipe)

### 4.3 Styling Guidelines
- Use web-safe fonts (e.g., Georgia, Arial, system fonts)
- Compact spacing and minimal margins for printing (0.2-inch margins)
- Small base font size (10pt) with reduced line height (1.3)
- Clear section headings with minimal spacing
- Two-column grid for ingredients with aligned measurements
- Ingredient format: quantity (bold, right-aligned) | unit | name | prep (italic)
- Print-friendly colors (avoid heavy backgrounds)
- Reduced padding and margins throughout to maximize space

### 4.4 HTML Template Structure
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>[Recipe Title] - Recipe Card</title>
    <style>
        @media print {
            @page { margin: 1in; }
            body { margin: 0; }
        }

        body {
            font-family: Georgia, 'Times New Roman', serif;
            line-height: 1.6;
            max-width: 8.5in;
            margin: 0 auto;
            padding: 1in;
            background: white;
            color: #333;
        }

        h1 {
            font-size: 2em;
            margin-bottom: 0.25em;
            color: #2c3e50;
            border-bottom: 3px solid #e74c3c;
            padding-bottom: 0.25em;
        }

        .metadata {
            font-size: 0.9em;
            color: #666;
            margin-bottom: 1.5em;
        }

        .metadata span {
            display: inline-block;
            margin-right: 1.5em;
        }

        h2 {
            font-size: 1.3em;
            color: #e74c3c;
            margin-top: 1.5em;
            margin-bottom: 0.5em;
            border-bottom: 1px solid #ddd;
            padding-bottom: 0.25em;
        }

        .description {
            font-style: italic;
            margin-bottom: 1.5em;
            padding: 0.5em;
            background: #f9f9f9;
            border-left: 3px solid #e74c3c;
        }

        .ingredients {
            margin-bottom: 1.5em;
        }

        .ingredients table {
            width: 100%;
            border-collapse: collapse;
        }

        .ingredients th {
            text-align: left;
            padding: 0.5em;
            background: #2c3e50;
            color: white;
            font-weight: normal;
        }

        .ingredients td {
            padding: 0.5em;
            border-bottom: 1px solid #eee;
        }

        .ingredients tr:last-child td {
            border-bottom: none;
        }

        .instructions {
            margin-bottom: 1.5em;
        }

        .instructions ol {
            padding-left: 1.5em;
        }

        .instructions li {
            margin-bottom: 0.75em;
        }

        .notes {
            background: #fffbea;
            padding: 1em;
            border-radius: 4px;
            margin-bottom: 1em;
        }

        .notes h3 {
            margin-top: 0;
            color: #e74c3c;
            font-size: 1.1em;
        }

        .notes ul {
            margin: 0.5em 0;
            padding-left: 1.5em;
        }

        .notes li {
            margin-bottom: 0.25em;
        }

        .footer {
            margin-top: 2em;
            padding-top: 1em;
            border-top: 1px solid #ddd;
            font-size: 0.85em;
            color: #666;
        }

        .footer a {
            color: #3498db;
            text-decoration: none;
        }

        @media print {
            .footer a {
                color: #666;
            }
        }
    </style>
</head>
<body>
    <!-- Recipe content populated from markdown -->
</body>
</html>
```

## Step 5: Parse Recipe Data
Extract and format the following from the markdown:
- **Title**: Extract from the `# [Title]` heading
- **Metadata**: Parse the bold key-value pairs (Source, Cuisine, Category, Servings, etc.)
- **Description**: Extract from the Description section
- **Ingredients**: Parse the table into HTML table format
- **Instructions**: Extract numbered steps and format as ordered list
- **Notes**: Extract both "Notes from Source" and "Personal Notes" sections if present
- **Tags**: Optional, can be shown in footer

## Step 6: Create the HTML File
Use the Write tool to create a file at `./recipes/[recipe-folder]/[recipe-name].html`

The HTML file should be saved in the same folder as the recipe markdown file.

Use the same filename as the recipe but change the extension to `.html`.

## Step 7: Optionally Generate PDF
After creating the HTML file, check if automatic PDF generation is available:

### 7.1 Check for Chrome/Chromium
Use Bash to check if Chrome is installed:
```bash
ls "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" 2>/dev/null || which google-chrome || which chromium
```

### 7.2 If Chrome is Available
Generate the PDF automatically using Chrome headless mode with minimal margins and no headers/footers:
```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless --disable-gpu --no-pdf-header-footer --print-to-pdf-no-header --print-to-pdf="recipes/[recipe-folder]/[filename].pdf" "file://$(pwd)/recipes/[recipe-folder]/[filename].html"
```

Then inform the user:
```
Successfully created recipe card for '[Recipe Title]':
- Markdown: [recipes/recipe-folder/filename.md](recipes/recipe-folder/filename.md)
- HTML: [recipes/recipe-folder/filename.html](recipes/recipe-folder/filename.html)
- PDF: [recipes/recipe-folder/filename.pdf](recipes/recipe-folder/filename.pdf)
```

### 7.3 If Chrome is Not Available
Check for alternative PDF generators:
```bash
which weasyprint || which wkhtmltopdf
```

**If weasyprint is available:**
```bash
weasyprint recipes/[recipe-folder]/[filename].html recipes/[recipe-folder]/[filename].pdf
```

**If wkhtmltopdf is available:**
```bash
wkhtmltopdf recipes/[recipe-folder]/[filename].html recipes/[recipe-folder]/[filename].pdf
```

**If no PDF generator is available:**
Provide manual instructions:
```
Successfully created recipe card for '[Recipe Title]' at [recipes/recipe-folder/filename.html](recipes/recipe-folder/filename.html)

To save as PDF:
1. Open the HTML file in your web browser
2. Press Cmd+P (Mac) or Ctrl+P (Windows) to print
3. Select "Save as PDF" as the destination
4. Save to your desired location

The recipe card is formatted for standard letter-size paper (8.5" × 11") with compact 0.2-inch margins to fit everything on one page.

---

Tip: For automatic PDF generation in the future:
- macOS: Install Google Chrome (most common, works with headless mode)
- Alternative: brew install weasyprint (Python-based HTML to PDF)
- Linux: Install chromium-browser or weasyprint
- Windows: Install Google Chrome or use browser print function
```
```

## Step 8: Confirm File Structure
Verify that all recipe files are now in the same folder:
- `recipes/[recipe-name]/[recipe-name].md` - Recipe markdown
- `recipes/[recipe-name]/[recipe-name].html` - Recipe card HTML
- `recipes/[recipe-name]/[recipe-name].pdf` - Recipe card PDF (if generated)

## Step 9: Handle Edge Cases
- If the recipe is very long (30+ steps), consider adding page break hints in the CSS
- If personal notes are empty, skip that section
- If no active time is specified, don't show "Active Time: N/A"
- Preserve any special formatting in instruction steps (bold, italic) if present
- **For quick staple recipes**: Adapt the HTML to handle flexible ingredient formats and high-level instructions gracefully. The recipe card can still be useful even without precise measurements.
