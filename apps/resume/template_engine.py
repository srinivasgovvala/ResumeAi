"""
Resume Template Engine
10 ATS-friendly single-column templates with full section support.
"""

# ─── Template definitions ────────────────────────────────────────────────────

TEMPLATES = {
    'classic': {
        'name': 'Classic Professional',
        'description': 'Traditional single-column layout trusted by Fortune 500 recruiters. Clean, proven, universally ATS-safe.',
        'best_for': 'All industries, all experience levels',
        'category': 'universal',
        'section_order_experienced': [
            'header', 'summary', 'experience', 'education', 'skills',
            'certifications', 'projects', 'awards', 'languages',
        ],
        'section_order_fresher': [
            'header', 'objective', 'education', 'skills', 'projects',
            'internships', 'certifications', 'awards', 'languages',
        ],
        'styles': {
            'font_family': 'Arial, Helvetica, sans-serif',
            'font_size': '10.5px',
            'line_height': '1.55',
            'name_size': '20px',
            'name_weight': '700',
            'name_color': '#0f172a',
            'accent_color': '#2563eb',
            'section_header_size': '10.5px',
            'section_header_weight': '700',
            'section_header_transform': 'uppercase',
            'section_header_color': '#0f172a',
            'section_divider': 'border-bottom: 1.5px solid #e2e8f0',
            'header_divider': 'border-top: 2px solid #2563eb',
            'contact_color': '#475569',
            'body_color': '#1e293b',
            'muted_color': '#64748b',
            'margin': '0.7in',
            'page_margin_top': '0.65in',
        },
        'pdf': {
            'name_size': 18, 'name_color': '#0f172a', 'accent': '#2563eb',
            'section_size': 10.5, 'body_size': 9.5, 'sub_size': 9,
            'left_margin': 0.7, 'right_margin': 0.7, 'top_margin': 0.65, 'bottom_margin': 0.6,
            'section_rule_color': '#e2e8f0', 'header_rule_color': '#2563eb',
            'header_rule_width': 2, 'section_rule_width': 0.75,
        },
    },

    'modern': {
        'name': 'Modern Minimal',
        'description': 'Clean whitespace-driven design with subtle left accent bar. Elegant and contemporary while remaining fully ATS-parseable.',
        'best_for': 'Tech, startups, product, design (non-graphic), finance',
        'category': 'modern',
        'section_order_experienced': [
            'header', 'summary', 'experience', 'skills', 'education',
            'projects', 'certifications', 'achievements', 'languages',
        ],
        'section_order_fresher': [
            'header', 'objective', 'skills', 'education', 'projects',
            'internships', 'certifications', 'languages',
        ],
        'styles': {
            'font_family': "'Georgia', 'Times New Roman', serif",
            'font_size': '10px',
            'line_height': '1.6',
            'name_size': '22px',
            'name_weight': '400',
            'name_color': '#0f172a',
            'accent_color': '#0ea5e9',
            'section_header_size': '9px',
            'section_header_weight': '700',
            'section_header_transform': 'uppercase',
            'section_header_color': '#0ea5e9',
            'section_divider': 'border-bottom: none',
            'header_divider': 'border-top: none',
            'contact_color': '#64748b',
            'body_color': '#1e293b',
            'muted_color': '#94a3b8',
            'margin': '0.75in',
            'page_margin_top': '0.65in',
            'name_letter_spacing': '2px',
        },
        'pdf': {
            'name_size': 20, 'name_color': '#0f172a', 'accent': '#0ea5e9',
            'section_size': 9.5, 'body_size': 9.5, 'sub_size': 9,
            'left_margin': 0.75, 'right_margin': 0.75, 'top_margin': 0.65, 'bottom_margin': 0.6,
            'section_rule_color': '#e2e8f0', 'header_rule_color': '#0ea5e9',
            'header_rule_width': 0, 'section_rule_width': 0,
        },
    },

    'corporate': {
        'name': 'Corporate',
        'description': 'Structured, formal layout preferred by banking, consulting, law, and enterprise organizations. Authoritative and polished.',
        'best_for': 'Banking, consulting, law, healthcare admin, corporate roles',
        'category': 'formal',
        'section_order_experienced': [
            'header', 'summary', 'experience', 'education', 'skills',
            'certifications', 'publications', 'awards', 'languages',
        ],
        'section_order_fresher': [
            'header', 'objective', 'education', 'internships', 'skills',
            'projects', 'certifications', 'awards', 'languages',
        ],
        'styles': {
            'font_family': "'Times New Roman', Georgia, serif",
            'font_size': '10.5px',
            'line_height': '1.5',
            'name_size': '18px',
            'name_weight': '700',
            'name_color': '#0f172a',
            'accent_color': '#1e3a5f',
            'section_header_size': '10.5px',
            'section_header_weight': '700',
            'section_header_transform': 'uppercase',
            'section_header_color': '#1e3a5f',
            'section_divider': 'border-bottom: 1px solid #1e3a5f',
            'header_divider': 'border-top: 2px solid #1e3a5f',
            'contact_color': '#374151',
            'body_color': '#111827',
            'muted_color': '#6b7280',
            'margin': '0.75in',
            'page_margin_top': '0.75in',
        },
        'pdf': {
            'name_size': 17, 'name_color': '#0f172a', 'accent': '#1e3a5f',
            'section_size': 10.5, 'body_size': 9.5, 'sub_size': 9,
            'left_margin': 0.75, 'right_margin': 0.75, 'top_margin': 0.75, 'bottom_margin': 0.65,
            'section_rule_color': '#1e3a5f', 'header_rule_color': '#1e3a5f',
            'header_rule_width': 2, 'section_rule_width': 0.75,
        },
    },

    'technical': {
        'name': 'Technical / Developer',
        'description': 'Optimized for software engineers and IT professionals. Highlights tech stacks, GitHub, and projects prominently.',
        'best_for': 'Software engineering, DevOps, data science, cybersecurity, QA',
        'category': 'technical',
        'section_order_experienced': [
            'header', 'summary', 'skills', 'experience', 'projects',
            'education', 'certifications', 'achievements', 'languages',
        ],
        'section_order_fresher': [
            'header', 'objective', 'skills', 'projects', 'education',
            'internships', 'certifications', 'achievements', 'languages',
        ],
        'styles': {
            'font_family': "'Courier New', 'Lucida Console', monospace",
            'font_size': '10px',
            'line_height': '1.5',
            'name_size': '19px',
            'name_weight': '700',
            'name_color': '#0f172a',
            'accent_color': '#16a34a',
            'section_header_size': '10px',
            'section_header_weight': '700',
            'section_header_transform': 'uppercase',
            'section_header_color': '#16a34a',
            'section_divider': 'border-bottom: 1px solid #dcfce7',
            'header_divider': 'border-top: 2px solid #16a34a',
            'contact_color': '#374151',
            'body_color': '#111827',
            'muted_color': '#6b7280',
            'margin': '0.65in',
            'page_margin_top': '0.6in',
        },
        'pdf': {
            'name_size': 17, 'name_color': '#0f172a', 'accent': '#16a34a',
            'section_size': 10, 'body_size': 9.5, 'sub_size': 9,
            'left_margin': 0.65, 'right_margin': 0.65, 'top_margin': 0.6, 'bottom_margin': 0.55,
            'section_rule_color': '#dcfce7', 'header_rule_color': '#16a34a',
            'header_rule_width': 2, 'section_rule_width': 0.5,
        },
    },

    'engineering': {
        'name': 'Engineering',
        'description': 'Precise, systematic layout for mechanical, civil, electrical, and chemical engineers. Emphasizes technical skills and project outcomes.',
        'best_for': 'Mechanical, civil, electrical, chemical engineering, R&D',
        'category': 'technical',
        'section_order_experienced': [
            'header', 'summary', 'skills', 'experience', 'projects',
            'education', 'certifications', 'publications', 'awards',
        ],
        'section_order_fresher': [
            'header', 'objective', 'education', 'skills', 'projects',
            'internships', 'certifications', 'achievements', 'languages',
        ],
        'styles': {
            'font_family': "'Arial', 'Helvetica Neue', sans-serif",
            'font_size': '10px',
            'line_height': '1.5',
            'name_size': '18px',
            'name_weight': '700',
            'name_color': '#1c1c1e',
            'accent_color': '#b45309',
            'section_header_size': '10px',
            'section_header_weight': '700',
            'section_header_transform': 'uppercase',
            'section_header_color': '#b45309',
            'section_divider': 'border-bottom: 1.5px solid #fef3c7',
            'header_divider': 'border-top: 2px solid #b45309',
            'contact_color': '#374151',
            'body_color': '#111827',
            'muted_color': '#6b7280',
            'margin': '0.7in',
            'page_margin_top': '0.65in',
        },
        'pdf': {
            'name_size': 17, 'name_color': '#1c1c1e', 'accent': '#b45309',
            'section_size': 10, 'body_size': 9.5, 'sub_size': 9,
            'left_margin': 0.7, 'right_margin': 0.7, 'top_margin': 0.65, 'bottom_margin': 0.6,
            'section_rule_color': '#fef3c7', 'header_rule_color': '#b45309',
            'header_rule_width': 2, 'section_rule_width': 0.75,
        },
    },

    'academic': {
        'name': 'Academic',
        'description': 'Detailed CV-style layout for researchers, academics, and PhD students. Publications, awards, and education take precedence.',
        'best_for': 'Academia, research, PhD positions, postdocs, faculty roles',
        'category': 'academic',
        'section_order_experienced': [
            'header', 'summary', 'education', 'experience', 'publications',
            'projects', 'skills', 'certifications', 'awards', 'languages', 'volunteer',
        ],
        'section_order_fresher': [
            'header', 'objective', 'education', 'projects', 'publications',
            'skills', 'certifications', 'awards', 'languages',
        ],
        'styles': {
            'font_family': "'Palatino Linotype', 'Book Antiqua', Palatino, serif",
            'font_size': '10.5px',
            'line_height': '1.6',
            'name_size': '20px',
            'name_weight': '700',
            'name_color': '#1a1a2e',
            'accent_color': '#4a1942',
            'section_header_size': '11px',
            'section_header_weight': '700',
            'section_header_transform': 'uppercase',
            'section_header_color': '#4a1942',
            'section_divider': 'border-bottom: 1px solid #4a1942',
            'header_divider': 'border-top: 1.5px solid #4a1942',
            'contact_color': '#374151',
            'body_color': '#1a1a2e',
            'muted_color': '#6b7280',
            'margin': '1in',
            'page_margin_top': '1in',
        },
        'pdf': {
            'name_size': 18, 'name_color': '#1a1a2e', 'accent': '#4a1942',
            'section_size': 11, 'body_size': 10, 'sub_size': 9.5,
            'left_margin': 1.0, 'right_margin': 1.0, 'top_margin': 1.0, 'bottom_margin': 0.8,
            'section_rule_color': '#4a1942', 'header_rule_color': '#4a1942',
            'header_rule_width': 1.5, 'section_rule_width': 0.75,
        },
    },

    'executive': {
        'name': 'Executive',
        'description': 'Premium executive-level layout for senior leaders, C-suite, and directors. Commands authority with refined typography.',
        'best_for': 'C-suite, VPs, Directors, Senior Managers, 10+ years experience',
        'category': 'formal',
        'section_order_experienced': [
            'header', 'summary', 'achievements', 'experience', 'education',
            'skills', 'certifications', 'publications', 'awards',
        ],
        'section_order_fresher': [
            'header', 'summary', 'education', 'experience', 'skills',
            'certifications', 'awards',
        ],
        'styles': {
            'font_family': "'Garamond', 'EB Garamond', Georgia, serif",
            'font_size': '11px',
            'line_height': '1.6',
            'name_size': '24px',
            'name_weight': '700',
            'name_color': '#111827',
            'accent_color': '#7c2d12',
            'section_header_size': '11px',
            'section_header_weight': '700',
            'section_header_transform': 'uppercase',
            'section_header_color': '#7c2d12',
            'section_divider': 'border-bottom: 1.5px solid #fef2ee',
            'header_divider': 'border-top: 2.5px solid #7c2d12',
            'contact_color': '#374151',
            'body_color': '#111827',
            'muted_color': '#6b7280',
            'margin': '0.85in',
            'page_margin_top': '0.8in',
        },
        'pdf': {
            'name_size': 22, 'name_color': '#111827', 'accent': '#7c2d12',
            'section_size': 11, 'body_size': 10, 'sub_size': 9.5,
            'left_margin': 0.85, 'right_margin': 0.85, 'top_margin': 0.8, 'bottom_margin': 0.7,
            'section_rule_color': '#fef2ee', 'header_rule_color': '#7c2d12',
            'header_rule_width': 2.5, 'section_rule_width': 1,
        },
    },

    'fresher': {
        'name': 'Fresher / Entry Level',
        'description': 'Optimized 1-page layout for students and new graduates. Puts education and skills front-and-center, maximizes limited experience.',
        'best_for': 'Fresh graduates, students, first job seekers, internship applicants',
        'category': 'entry',
        'section_order_experienced': [
            'header', 'objective', 'education', 'skills', 'projects',
            'internships', 'certifications', 'awards', 'languages',
        ],
        'section_order_fresher': [
            'header', 'objective', 'education', 'skills', 'projects',
            'internships', 'certifications', 'awards', 'languages',
        ],
        'styles': {
            'font_family': "'Calibri', 'Trebuchet MS', Arial, sans-serif",
            'font_size': '10px',
            'line_height': '1.5',
            'name_size': '21px',
            'name_weight': '700',
            'name_color': '#1e293b',
            'accent_color': '#0891b2',
            'section_header_size': '10px',
            'section_header_weight': '700',
            'section_header_transform': 'uppercase',
            'section_header_color': '#0891b2',
            'section_divider': 'border-bottom: 1.5px solid #cffafe',
            'header_divider': 'border-top: 2px solid #0891b2',
            'contact_color': '#475569',
            'body_color': '#1e293b',
            'muted_color': '#64748b',
            'margin': '0.6in',
            'page_margin_top': '0.6in',
        },
        'pdf': {
            'name_size': 19, 'name_color': '#1e293b', 'accent': '#0891b2',
            'section_size': 10, 'body_size': 9.5, 'sub_size': 9,
            'left_margin': 0.6, 'right_margin': 0.6, 'top_margin': 0.6, 'bottom_margin': 0.55,
            'section_rule_color': '#cffafe', 'header_rule_color': '#0891b2',
            'header_rule_width': 2, 'section_rule_width': 0.75,
        },
    },

    'creative': {
        'name': 'Creative Professional',
        'description': 'Bold name treatment with tasteful accent lines. Stands out visually while staying fully machine-readable for ATS systems.',
        'best_for': 'Marketing, PR, content, UX writing, communications, advertising',
        'category': 'modern',
        'section_order_experienced': [
            'header', 'summary', 'experience', 'skills', 'projects',
            'education', 'certifications', 'achievements', 'volunteer', 'languages',
        ],
        'section_order_fresher': [
            'header', 'objective', 'skills', 'education', 'projects',
            'internships', 'certifications', 'achievements', 'languages',
        ],
        'styles': {
            'font_family': "'Verdana', 'Tahoma', Geneva, sans-serif",
            'font_size': '10px',
            'line_height': '1.55',
            'name_size': '23px',
            'name_weight': '700',
            'name_color': '#1e1b4b',
            'accent_color': '#7c3aed',
            'section_header_size': '10px',
            'section_header_weight': '700',
            'section_header_transform': 'uppercase',
            'section_header_color': '#7c3aed',
            'section_divider': 'border-bottom: 1px solid #ede9fe',
            'header_divider': 'border-top: 3px solid #7c3aed',
            'contact_color': '#4c4f69',
            'body_color': '#1e1b4b',
            'muted_color': '#6d6d85',
            'margin': '0.7in',
            'page_margin_top': '0.65in',
        },
        'pdf': {
            'name_size': 21, 'name_color': '#1e1b4b', 'accent': '#7c3aed',
            'section_size': 10, 'body_size': 9.5, 'sub_size': 9,
            'left_margin': 0.7, 'right_margin': 0.7, 'top_margin': 0.65, 'bottom_margin': 0.6,
            'section_rule_color': '#ede9fe', 'header_rule_color': '#7c3aed',
            'header_rule_width': 3, 'section_rule_width': 0.5,
        },
    },

    'compact': {
        'name': 'Compact',
        'description': 'Maximum information density for experienced professionals with 10+ years. Tight spacing ensures everything fits in 1-2 pages.',
        'best_for': 'Experienced professionals, career changers, anyone with dense work history',
        'category': 'compact',
        'section_order_experienced': [
            'header', 'summary', 'experience', 'skills', 'education',
            'projects', 'certifications', 'achievements', 'awards', 'languages', 'volunteer',
        ],
        'section_order_fresher': [
            'header', 'objective', 'education', 'skills', 'projects',
            'internships', 'certifications', 'awards', 'languages',
        ],
        'styles': {
            'font_family': "'Arial Narrow', 'Arial', sans-serif",
            'font_size': '9.5px',
            'line_height': '1.45',
            'name_size': '17px',
            'name_weight': '700',
            'name_color': '#0f172a',
            'accent_color': '#0369a1',
            'section_header_size': '9.5px',
            'section_header_weight': '700',
            'section_header_transform': 'uppercase',
            'section_header_color': '#0369a1',
            'section_divider': 'border-bottom: 1px solid #e0f2fe',
            'header_divider': 'border-top: 1.5px solid #0369a1',
            'contact_color': '#475569',
            'body_color': '#0f172a',
            'muted_color': '#64748b',
            'margin': '0.5in',
            'page_margin_top': '0.5in',
        },
        'pdf': {
            'name_size': 15, 'name_color': '#0f172a', 'accent': '#0369a1',
            'section_size': 9.5, 'body_size': 9, 'sub_size': 8.5,
            'left_margin': 0.5, 'right_margin': 0.5, 'top_margin': 0.5, 'bottom_margin': 0.45,
            'section_rule_color': '#e0f2fe', 'header_rule_color': '#0369a1',
            'header_rule_width': 1.5, 'section_rule_width': 0.5,
        },
    },

    'data_ai': {
        'name': 'Data & AI',
        'description': 'Tailored for data scientists, ML engineers, and AI researchers. Highlights quantitative skills, tools, and model performance metrics.',
        'best_for': 'Data science, machine learning, AI research, analytics, NLP, computer vision',
        'category': 'technical',
        'section_order_experienced': [
            'header', 'summary', 'skills', 'experience', 'projects',
            'education', 'certifications', 'publications', 'achievements', 'awards',
        ],
        'section_order_fresher': [
            'header', 'objective', 'skills', 'education', 'projects',
            'internships', 'certifications', 'achievements', 'languages',
        ],
        'styles': {
            'font_family': "'Roboto', 'Segoe UI', Arial, sans-serif",
            'font_size': '10px',
            'line_height': '1.55',
            'name_size': '20px',
            'name_weight': '700',
            'name_color': '#0c1a3a',
            'accent_color': '#1d4ed8',
            'section_header_size': '10px',
            'section_header_weight': '700',
            'section_header_transform': 'uppercase',
            'section_header_color': '#1d4ed8',
            'section_divider': 'border-bottom: 1.5px solid #dbeafe',
            'header_divider': 'border-top: 2px solid #1d4ed8',
            'contact_color': '#374151',
            'body_color': '#0c1a3a',
            'muted_color': '#6b7280',
            'margin': '0.65in',
            'page_margin_top': '0.6in',
        },
        'pdf': {
            'name_size': 18, 'name_color': '#0c1a3a', 'accent': '#1d4ed8',
            'section_size': 10, 'body_size': 9.5, 'sub_size': 9,
            'left_margin': 0.65, 'right_margin': 0.65, 'top_margin': 0.6, 'bottom_margin': 0.55,
            'section_rule_color': '#dbeafe', 'header_rule_color': '#1d4ed8',
            'header_rule_width': 2, 'section_rule_width': 0.75,
        },
    },

    'finance': {
        'name': 'Finance & Banking',
        'description': 'Conservative, authoritative layout for financial professionals. Structured and polished — ideal for Wall Street, Big Four, and corporate finance roles.',
        'best_for': 'Investment banking, accounting, financial analysis, auditing, CFA/CPA holders',
        'category': 'formal',
        'section_order_experienced': [
            'header', 'summary', 'experience', 'education', 'skills',
            'certifications', 'achievements', 'awards', 'languages',
        ],
        'section_order_fresher': [
            'header', 'objective', 'education', 'internships', 'skills',
            'projects', 'certifications', 'awards', 'languages',
        ],
        'styles': {
            'font_family': "'Book Antiqua', 'Palatino Linotype', Georgia, serif",
            'font_size': '10.5px',
            'line_height': '1.5',
            'name_size': '19px',
            'name_weight': '700',
            'name_color': '#0f172a',
            'accent_color': '#14532d',
            'section_header_size': '10.5px',
            'section_header_weight': '700',
            'section_header_transform': 'uppercase',
            'section_header_color': '#14532d',
            'section_divider': 'border-bottom: 1px solid #14532d',
            'header_divider': 'border-top: 2px solid #14532d',
            'contact_color': '#374151',
            'body_color': '#0f172a',
            'muted_color': '#6b7280',
            'margin': '0.8in',
            'page_margin_top': '0.75in',
        },
        'pdf': {
            'name_size': 17, 'name_color': '#0f172a', 'accent': '#14532d',
            'section_size': 10.5, 'body_size': 9.5, 'sub_size': 9,
            'left_margin': 0.8, 'right_margin': 0.8, 'top_margin': 0.75, 'bottom_margin': 0.65,
            'section_rule_color': '#14532d', 'header_rule_color': '#14532d',
            'header_rule_width': 2, 'section_rule_width': 0.75,
        },
    },

    'healthcare': {
        'name': 'Healthcare',
        'description': 'Clean, professional layout for clinical and healthcare roles. Prioritizes certifications, licenses, clinical experience, and education.',
        'best_for': 'Nurses, physicians, pharmacists, allied health, clinical research, medical admin',
        'category': 'formal',
        'section_order_experienced': [
            'header', 'summary', 'experience', 'certifications', 'education',
            'skills', 'achievements', 'publications', 'awards', 'languages',
        ],
        'section_order_fresher': [
            'header', 'objective', 'education', 'certifications', 'internships',
            'skills', 'projects', 'awards', 'languages',
        ],
        'styles': {
            'font_family': "'Calibri', 'Trebuchet MS', Arial, sans-serif",
            'font_size': '10.5px',
            'line_height': '1.55',
            'name_size': '19px',
            'name_weight': '700',
            'name_color': '#0f172a',
            'accent_color': '#0e7490',
            'section_header_size': '10.5px',
            'section_header_weight': '700',
            'section_header_transform': 'uppercase',
            'section_header_color': '#0e7490',
            'section_divider': 'border-bottom: 1.5px solid #cffafe',
            'header_divider': 'border-top: 2px solid #0e7490',
            'contact_color': '#374151',
            'body_color': '#0f172a',
            'muted_color': '#6b7280',
            'margin': '0.75in',
            'page_margin_top': '0.7in',
        },
        'pdf': {
            'name_size': 17, 'name_color': '#0f172a', 'accent': '#0e7490',
            'section_size': 10.5, 'body_size': 9.5, 'sub_size': 9,
            'left_margin': 0.75, 'right_margin': 0.75, 'top_margin': 0.7, 'bottom_margin': 0.6,
            'section_rule_color': '#cffafe', 'header_rule_color': '#0e7490',
            'header_rule_width': 2, 'section_rule_width': 0.75,
        },
    },

    'leadership': {
        'name': 'Leadership & Operations',
        'description': 'Bold, results-focused layout for team leaders, project managers, and operations professionals. Emphasizes impact, scope, and leadership metrics.',
        'best_for': 'Project managers, team leads, operations, HR, supply chain, program managers',
        'category': 'formal',
        'section_order_experienced': [
            'header', 'summary', 'achievements', 'experience', 'skills',
            'education', 'certifications', 'awards', 'volunteer', 'languages',
        ],
        'section_order_fresher': [
            'header', 'objective', 'education', 'skills', 'internships',
            'projects', 'certifications', 'achievements', 'languages',
        ],
        'styles': {
            'font_family': "'Arial', 'Helvetica Neue', sans-serif",
            'font_size': '10.5px',
            'line_height': '1.55',
            'name_size': '21px',
            'name_weight': '700',
            'name_color': '#1e1b4b',
            'accent_color': '#4338ca',
            'section_header_size': '10.5px',
            'section_header_weight': '700',
            'section_header_transform': 'uppercase',
            'section_header_color': '#4338ca',
            'section_divider': 'border-bottom: 2px solid #4338ca',
            'header_divider': 'border-top: 3px solid #4338ca',
            'contact_color': '#374151',
            'body_color': '#1e1b4b',
            'muted_color': '#6b7280',
            'margin': '0.75in',
            'page_margin_top': '0.7in',
        },
        'pdf': {
            'name_size': 19, 'name_color': '#1e1b4b', 'accent': '#4338ca',
            'section_size': 10.5, 'body_size': 9.5, 'sub_size': 9,
            'left_margin': 0.75, 'right_margin': 0.75, 'top_margin': 0.7, 'bottom_margin': 0.6,
            'section_rule_color': '#e0e7ff', 'header_rule_color': '#4338ca',
            'header_rule_width': 3, 'section_rule_width': 1,
        },
    },

    'minimal': {
        'name': 'Clean Minimal',
        'description': 'Pure typographic layout with zero color. Maximum ATS safety — zero formatting risk. Works for any role or industry.',
        'best_for': 'Any role — maximum ATS safety, conservative industries, career changers',
        'category': 'universal',
        'section_order_experienced': [
            'header', 'summary', 'experience', 'education', 'skills',
            'projects', 'certifications', 'awards', 'languages',
        ],
        'section_order_fresher': [
            'header', 'objective', 'education', 'skills', 'projects',
            'internships', 'certifications', 'awards', 'languages',
        ],
        'styles': {
            'font_family': "'Arial', Helvetica, sans-serif",
            'font_size': '10.5px',
            'line_height': '1.5',
            'name_size': '18px',
            'name_weight': '700',
            'name_color': '#000000',
            'accent_color': '#000000',
            'section_header_size': '10.5px',
            'section_header_weight': '700',
            'section_header_transform': 'uppercase',
            'section_header_color': '#000000',
            'section_divider': 'border-bottom: 1px solid #000000',
            'header_divider': 'border-top: 1px solid #000000',
            'contact_color': '#333333',
            'body_color': '#000000',
            'muted_color': '#555555',
            'margin': '0.75in',
            'page_margin_top': '0.75in',
        },
        'pdf': {
            'name_size': 16, 'name_color': '#000000', 'accent': '#000000',
            'section_size': 10.5, 'body_size': 9.5, 'sub_size': 9,
            'left_margin': 0.75, 'right_margin': 0.75, 'top_margin': 0.75, 'bottom_margin': 0.65,
            'section_rule_color': '#000000', 'header_rule_color': '#000000',
            'header_rule_width': 1, 'section_rule_width': 0.5,
        },
    },
}


def get_all_templates() -> dict:
    """
    Returns dictionary of all templates, merging built-in TEMPLATES with active DB ResumeTemplate instances.
    Enables Admin users to add or edit templates directly in Django Admin.
    """
    all_tpls = {k: v.copy() for k, v in TEMPLATES.items()}
    try:
        from .models import ResumeTemplate
        db_templates = ResumeTemplate.objects.filter(is_active=True)
        for tpl in db_templates:
            slug = tpl.slug
            base = all_tpls.get(slug, {})
            entry = {
                'name': tpl.name,
                'description': tpl.description or base.get('description', ''),
                'best_for': tpl.best_for or base.get('best_for', ''),
                'category': tpl.category or base.get('category', 'universal'),
                'section_order_experienced': tpl.section_order_experienced if tpl.section_order_experienced else base.get('section_order_experienced', [
                    'header', 'summary', 'experience', 'education', 'skills',
                    'certifications', 'projects', 'awards', 'languages'
                ]),
                'section_order_fresher': tpl.section_order_fresher if tpl.section_order_fresher else base.get('section_order_fresher', [
                    'header', 'objective', 'education', 'skills', 'projects',
                    'internships', 'certifications', 'awards', 'languages'
                ]),
                'styles': tpl.styles if tpl.styles else base.get('styles', {
                    'font_family': 'Arial, Helvetica, sans-serif',
                    'font_size': '10.5px',
                    'line_height': '1.55',
                    'name_size': '20px',
                    'name_weight': '700',
                    'name_color': '#0f172a',
                    'accent_color': '#2563eb',
                    'section_header_size': '10.5px',
                    'section_header_weight': '700',
                    'section_header_transform': 'uppercase',
                    'section_header_color': '#0f172a',
                    'section_divider': 'border-bottom: 1.5px solid #e2e8f0',
                    'header_divider': 'border-top: 2px solid #2563eb',
                    'contact_color': '#475569',
                    'body_color': '#1e293b',
                    'muted_color': '#64748b',
                    'margin': '0.7in',
                    'page_margin_top': '0.65in',
                }),
                'pdf': tpl.pdf_config if tpl.pdf_config else base.get('pdf', {
                    'name_size': 18, 'name_color': '#0f172a', 'accent': '#2563eb',
                    'section_size': 10.5, 'body_size': 9.5, 'sub_size': 9,
                    'left_margin': 0.7, 'right_margin': 0.7, 'top_margin': 0.65, 'bottom_margin': 0.6,
                    'section_rule_color': '#e2e8f0', 'header_rule_color': '#2563eb',
                    'header_rule_width': 2, 'section_rule_width': 0.75,
                }),
            }
            all_tpls[slug] = entry
    except Exception:
        pass
    return all_tpls


def get_template_config(template_style: str, customization: dict = None) -> dict:
    """Return template config with optional user customization overrides."""
    all_tpls = get_all_templates()
    config = all_tpls.get(template_style, all_tpls.get('classic', TEMPLATES['classic'])).copy()
    if customization:
        styles = config['styles'].copy()
        pdf = config['pdf'].copy()
        if customization.get('accent_color'):
            styles['accent_color'] = customization['accent_color']
            styles['section_header_color'] = customization['accent_color']
            pdf['accent'] = customization['accent_color']
        if customization.get('font_family'):
            styles['font_family'] = customization['font_family']
        if customization.get('font_size'):
            styles['font_size'] = customization['font_size']
            try:
                pdf['body_size'] = float(customization['font_size'].replace('px', ''))
            except Exception:
                pass
        if customization.get('line_height'):
            styles['line_height'] = customization['line_height']
        config['styles'] = styles
        config['pdf'] = pdf
    return config


def get_section_order(template_style: str, is_fresher: bool) -> list:
    all_tpls = get_all_templates()
    config = all_tpls.get(template_style, all_tpls.get('classic', TEMPLATES['classic']))
    if is_fresher:
        return config.get('section_order_fresher', config['section_order_experienced'])
    return config.get('section_order_experienced')


def detect_fresher(resume) -> bool:
    """Heuristic: no work experience or only internships → fresher."""
    exp = resume.experience if hasattr(resume, 'experience') else resume.get('experience', [])
    if isinstance(exp, list) and len(exp) > 0:
        return False
    return True


def get_template_recommendations(template_style: str, is_fresher: bool) -> list:
    recs = []
    if is_fresher:
        recs += [
            'Keep your resume to 1 page — recruiters expect this for entry-level roles.',
            'Lead with Education and Projects since you have limited work experience.',
            'Add 2–3 academic or personal projects with clear technology stacks.',
            'Include relevant coursework, GPA (if ≥ 3.5), and academic honors.',
            'Internships and part-time roles count — add them under Internships.',
            'List 8–12 specific technical and soft skills relevant to the role.',
            'Use a strong Career Objective (3–4 sentences) tailored to each application.',
        ]
    else:
        recs += [
            'Open with a strong 3–4 sentence Professional Summary with key metrics.',
            'Lead with your most recent and relevant work experience.',
            'Quantify achievements with numbers (%, $, time saved) wherever possible.',
            'Tailor skills to match the job description keywords for better ATS ranking.',
            'Include certifications with issuer name and year for credibility.',
            'A 2-page resume is acceptable for 7+ years of experience.',
            'Remove experience older than 15 years unless it is highly relevant.',
        ]
    template_tips = {
        'technical': ['Put your GitHub URL in the header — recruiters will check it.',
                      'Group skills by category (Languages, Frameworks, Tools, Cloud).'],
        'academic': ['Include all publications with full citations in standard format.',
                     'List grants, funding, and conference presentations separately.'],
        'executive': ['Lead with Achievements section highlighting measurable business impact.',
                      'Each bullet should show scope of responsibility and outcome.'],
        'creative': ['Mention key campaigns, launches, or creative projects with results.',
                     'Include portfolio URL prominently in the header.'],
        'compact': ['Use tight bullets — 1 line each is ideal for density.',
                    'Cut roles older than 12 years to keep to 2 pages maximum.'],
        'fresher': ['Use a Career Objective instead of Summary — it signals your goals.',
                    'Include all relevant coursework and academic projects.'],
        'data_ai': ['Include GitHub, Kaggle, or HuggingFace profile links in the header.',
                    'Quantify model performance: accuracy %, latency ms, dataset size.'],
        'finance': ['Include CFA, CPA, or FRM credential prominently near your name.',
                    'Every bullet should quantify financial impact: revenue, cost, portfolio size.'],
        'healthcare': ['List all active licenses and certifications with expiry dates.',
                       'Include clinical specialties and EHR systems you are proficient in.'],
        'leadership': ['Lead every bullet with scope: "Led team of X", "Managed $Xm budget".',
                       'Include cross-functional collaboration and stakeholder management examples.'],
        'minimal': ['Every word counts — remove filler phrases like "responsible for".',
                    'Use clean action verbs and quantified outcomes throughout.'],
    }
    recs += template_tips.get(template_style, [])
    return recs


def validate_ats(resume_data: dict) -> list:
    """Return list of ATS warnings. Empty list = no issues."""
    warnings = []
    d = resume_data

    # Contact completeness
    if not d.get('full_name', '').strip():
        warnings.append({'level': 'error', 'msg': 'Missing full name — required for every resume.'})
    if not d.get('email', '').strip():
        warnings.append({'level': 'error', 'msg': 'Missing email address — required for every resume.'})
    if not d.get('phone', '').strip():
        warnings.append({'level': 'warning', 'msg': 'No phone number found. Most employers expect one.'})

    # Section structure
    has_exp = bool(d.get('experience') or d.get('internships'))
    has_edu = bool(d.get('education'))
    if not has_edu:
        warnings.append({'level': 'error', 'msg': 'No education section — all resumes need at least one education entry.'})
    if not has_exp:
        warnings.append({'level': 'info', 'msg': 'No work experience or internships. Consider adding projects to demonstrate skills.'})

    summary = d.get('professional_summary', '') or d.get('career_objective', '')
    if not summary.strip():
        warnings.append({'level': 'warning', 'msg': 'No summary or objective. A 3–4 sentence opening dramatically improves ATS ranking.'})

    skills = d.get('skills', [])
    if not skills:
        warnings.append({'level': 'error', 'msg': 'No skills listed — the Skills section is the #1 ATS keyword source.'})
    elif len(skills) < 5:
        warnings.append({'level': 'warning', 'msg': f'Only {len(skills)} skills listed. Aim for 8–12 for best ATS coverage.'})

    # Content quality checks
    name = d.get('full_name', '')
    if any(c in name for c in ['|', '/', '\\', '<', '>']):
        warnings.append({'level': 'warning', 'msg': 'Unsupported characters in name. Use plain text only.'})

    total_words = 0
    for exp in d.get('experience', []):
        bullets = exp.get('bullets', [])
        if isinstance(bullets, list):
            total_words += sum(len(b.split()) for b in bullets)
        elif isinstance(bullets, str):
            total_words += len(bullets.split())
    total_words += len((summary).split())
    if total_words > 0 and total_words < 150:
        warnings.append({'level': 'warning', 'msg': f'Resume content is thin ({total_words} words). ATS systems favor 300–600 words.'})
    if total_words > 1000:
        warnings.append({'level': 'warning', 'msg': f'Resume may be too long ({total_words} words). Trim to 2 pages maximum.'})

    # Internship bullets quality
    for intern in d.get('internships', []):
        bullets = intern.get('bullets', [])
        if isinstance(bullets, str):
            bullets = [b for b in bullets.split('\n') if b.strip()]
        if len(bullets) == 0:
            warnings.append({'level': 'warning', 'msg': f'Internship at "{intern.get("company","")}" has no bullet points. Add 2–3 achievement-focused bullets.'})

    # Projects — check for empty descriptions
    for proj in d.get('projects', []):
        if not proj.get('description', '').strip():
            warnings.append({'level': 'warning', 'msg': f'Project "{proj.get("name","")}" has no description. Add measurable outcomes.'})

    # Certifications — check for issuer
    for cert in d.get('certifications', []):
        if isinstance(cert, dict) and cert.get('name') and not cert.get('issuer', '').strip():
            warnings.append({'level': 'info', 'msg': f'Certification "{cert["name"]}" has no issuing organization. Adding it boosts credibility.'})

    # LinkedIn check
    if not d.get('linkedin_url', '').strip():
        warnings.append({'level': 'info', 'msg': 'No LinkedIn URL. Adding one increases recruiter response rate by ~40%.'})

    # Skills count for flat list and dict format
    if isinstance(skills, dict):
        flat = [s for cat in skills.values() for s in (cat if isinstance(cat, list) else [])]
        if not flat:
            warnings.append({'level': 'error', 'msg': 'No skills listed — the Skills section is the #1 ATS keyword source.'})
        elif len(flat) < 5:
            warnings.append({'level': 'warning', 'msg': f'Only {len(flat)} skills listed. Aim for 8–12 for best ATS coverage.'})

    return warnings
