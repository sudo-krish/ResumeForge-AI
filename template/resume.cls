%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% 2025 Modern Professional Resume - OPTIMIZED FOR ATS & VISUAL APPEAL
%
% Designed for Data Engineers, Software Engineers, and Tech Professionals
% ATS-Friendly | Clean Design | Professional Typography
%
% Optimized by: 2025 Resume Standards
% Based on: Trey Hunner's Resume Class (Modified)
%
% Key Features:
% - Single column layout (ATS-friendly)
% - Modern typography with subtle accents
% - Improved spacing and readability
% - Hyperlinked contact info
% - Clean section separators
% - Professional bullet points
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\ProvidesClass{resume}[2025/11/12 v2.0 Modern Resume class]

\LoadClass[11pt,letterpaper]{article} % Standard font size and paper

%----------------------------------------------------------------------------------------
%   REQUIRED PACKAGES
%----------------------------------------------------------------------------------------

\usepackage[parfill]{parskip} % Remove paragraph indentation
\usepackage{array} % Enhanced table functionality
\usepackage{ifthen} % Conditional statements
\usepackage{hyperref} % Hyperlinks (critical for modern resumes)
\usepackage{xcolor} % Colors (used minimally for professionalism)
\usepackage{enumitem} % Better list control
\usepackage{fontawesome5} % Modern icons (optional, comment out if not available)
\usepackage[T1]{fontenc} % Better font encoding
\usepackage{lmodern} % Modern font family

%----------------------------------------------------------------------------------------
%   PAGE LAYOUT & MARGINS (ATS-Friendly)
%----------------------------------------------------------------------------------------

\usepackage[
    left=0.5in,
    right=0.5in,
    top=0.5in,
    bottom=0.5in
]{geometry}

\pagestyle{empty} % No page numbers (cleaner look)

%----------------------------------------------------------------------------------------
%   COLORS (Subtle, Professional)
%----------------------------------------------------------------------------------------

\definecolor{primarycolor}{RGB}{0, 0, 0}        % Black for text
\definecolor{accentcolor}{RGB}{0, 102, 204}    % Professional blue for accents
\definecolor{sectioncolor}{RGB}{47, 79, 79}    % Dark slate gray for sections
\definecolor{linkcolor}{RGB}{0, 102, 204}      % Blue for links

%----------------------------------------------------------------------------------------
%   HYPERLINK SETUP (ATS-Friendly)
%----------------------------------------------------------------------------------------

\hypersetup{
    colorlinks=true,
    linkcolor=linkcolor,
    filecolor=linkcolor,
    urlcolor=linkcolor,
    citecolor=primarycolor,
    pdfborder={0 0 0},        % No boxes around links
    pdfauthor={Your Name},
    pdftitle={Resume - Your Name}
}

%----------------------------------------------------------------------------------------
%   TYPOGRAPHY & SPACING
%----------------------------------------------------------------------------------------

\setlength{\parindent}{0pt}           % No paragraph indentation
\setlength{\parskip}{0pt}             % Minimal paragraph spacing

% Improved list spacing
\setlist{nosep, leftmargin=1.2em}
\setlist[itemize]{label=\textbullet, itemsep=2pt, parsep=0pt}

%----------------------------------------------------------------------------------------
%   NAME & CONTACT HEADER
%----------------------------------------------------------------------------------------

\def\name#1{\def\@name{#1}}
\def\@name{}

\def\addressSep{\textbar}  % Use pipe separator (modern look)

% Address lines
\let\@addressone\relax
\let\@addresstwo\relax
\let\@addressthree\relax

\def\address#1{%
  \@ifundefined{@addresstwo}{%
    \def\@addresstwo{#1}%
  }{%
  \@ifundefined{@addressone}{%
    \def\@addressone{#1}%
  }{%
    \def\@addressthree{#1}%
  }}%
}

% Print address with improved formatting
\def\printaddress#1{%
  \begingroup
    \def\\{\addressSep\space}%
    \centerline{\small #1}%
  \endgroup
  \par
  \smallskip
}

% Print name (larger, bolder, centered)
\def\printname{%
  \begingroup
    \centering
    {\Huge\bfseries\scshape\@name}\\[8pt]
  \endgroup
}

%----------------------------------------------------------------------------------------
%   DOCUMENT BEGIN (Header Generation)
%----------------------------------------------------------------------------------------

\let\ori@document=\document
\renewcommand{\document}{%
  \ori@document
  \printname
  \@ifundefined{@addressone}{}{%
    \printaddress{\@addressone}%
  }%
  \@ifundefined{@addresstwo}{}{%
    \printaddress{\@addresstwo}%
  }%
  \@ifundefined{@addressthree}{}{%
    \printaddress{\@addressthree}%
  }%
  \vspace{6pt}%
  \noindent\makebox[\linewidth]{\color{sectioncolor}\rule{\textwidth}{0.4pt}}%
  \vspace{4pt}%
}

%----------------------------------------------------------------------------------------
%   SECTION FORMATTING (Modern, Clean)
%----------------------------------------------------------------------------------------

\newenvironment{rSection}[1]{%
  \vspace{8pt}%
  \noindent{\large\bfseries\color{sectioncolor}\MakeUppercase{#1}}%
  \vspace{3pt}%
  \par\noindent\makebox[\linewidth]{\color{sectioncolor}\rule{\textwidth}{0.6pt}}%
  \vspace{4pt}%
  \begin{list}{}{%
    \setlength{\leftmargin}{0em}%
    \setlength{\itemindent}{0em}%
    \setlength{\itemsep}{0pt}%
    \setlength{\parsep}{0pt}%
  }%
  \item[]%
}{%
  \end{list}%
  \vspace{2pt}%
}

%----------------------------------------------------------------------------------------
%   SUBSECTION (Experience, Education, Projects)
%----------------------------------------------------------------------------------------

% 4 parameters: Title, Date, Subtitle, Location
\newenvironment{rSubsection}[4]{%
  \vspace{4pt}%
  \textbf{#1} \hfill \textbf{#2}%
  \ifthenelse{\equal{#3}{}}{}{%
    \\[2pt]%
    \textit{#3} \hfill \textit{#4}%
  }%
  \smallskip%
  \begin{itemize}[leftmargin=1.2em, itemsep=2pt, parsep=0pt]%
}{%
  \end{itemize}%
  \vspace{6pt}%
}

%----------------------------------------------------------------------------------------
%   COMPACT SUBSECTION (For Education/Certifications)
%----------------------------------------------------------------------------------------

\newenvironment{rSubsectionCompact}[4]{%
  \vspace{2pt}%
  \textbf{#1} \hfill \textbf{#2}%
  \ifthenelse{\equal{#3}{}}{}{%
    \\[2pt]%
    #3 \hfill \textit{#4}%
  }%
  \vspace{4pt}%
}{%
}

%----------------------------------------------------------------------------------------
%   SKILLS SECTION (Table-based, clean)
%----------------------------------------------------------------------------------------

\newenvironment{skillsTable}{%
  \vspace{2pt}%
  \begin{tabular*}{\textwidth}{@{\extracolsep{\fill}}p{0.22\textwidth}p{0.75\textwidth}}%
}{%
  \end{tabular*}%
  \vspace{4pt}%
}

%----------------------------------------------------------------------------------------
%   PROJECTS SECTION (With links)
%----------------------------------------------------------------------------------------

\newcommand{\projectItem}[4]{%
  \vspace{4pt}%
  \textbf{#1} \ifthenelse{\equal{#2}{}}{}{\hfill \href{#2}{\small\underline{GitHub}}}\\[2pt]%
  #3\\[2pt]%
  \textit{\small Technologies: #4}%
  \vspace{4pt}%
}

%----------------------------------------------------------------------------------------
%   CUSTOM COMMANDS & HELPERS
%----------------------------------------------------------------------------------------

% Contact line with icons (optional - comment out \usepackage{fontawesome5} if not available)
\newcommand{\contactLine}[4]{%
  \centerline{%
    \faPhone\space#1 \addressSep\space
    \faEnvelope\space\href{mailto:#2}{#2} \addressSep\space
    \faLinkedin\space\href{#3}{LinkedIn} \addressSep\space
    \faGithub\space\href{#4}{GitHub}%
  }%
}

% Simple contact line (no icons, ATS-safe)
\newcommand{\contactLineSimple}[4]{%
  \centerline{%
    #1 \addressSep\space
    \href{mailto:#2}{#2} \addressSep\space
    \href{#3}{LinkedIn} \addressSep\space
    \href{#4}{GitHub}%
  }%
}

%----------------------------------------------------------------------------------------
%   SPACING DEFINITIONS (Fine-tuned for readability)
%----------------------------------------------------------------------------------------

\def\nameskip{\vspace{4pt}}
\def\addressskip{\vspace{2pt}}
\def\sectionlineskip{\vspace{3pt}}
\def\sectionskip{\vspace{8pt}}

%----------------------------------------------------------------------------------------
%   DOCUMENT SETTINGS
%----------------------------------------------------------------------------------------

% Prevent widows and orphans (better page breaks)
\widowpenalty=10000
\clubpenalty=10000

% Better list bullets
\renewcommand{\labelitemi}{\textbullet}
\renewcommand{\labelitemii}{\textendash}

%----------------------------------------------------------------------------------------
%   END OF CLASS FILE
%----------------------------------------------------------------------------------------
