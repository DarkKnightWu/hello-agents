#!/usr/bin/env python3
import os
import re
import subprocess
import sys
from urllib.parse import unquote

def merge_markdown_files(sidebar_path, base_dir, output_path):
    print(f"Reading sidebar from {sidebar_path}...")
    if not os.path.exists(sidebar_path):
        print(f"Error: Sidebar file not found at {sidebar_path}")
        return False

    with open(sidebar_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find all links in the format [Title](Path)
    # Example: - [第一章 初识智能体](./chapter1/第一章%20初识智能体.md)
    links = re.findall(r'\[(.*?)\]\((.*?)\)', content)
    
    if not links:
        print("Error: No links found in sidebar.")
        return False
        
    print(f"Found {len(links)} linked files.")
    
    merged_content = []
    
    # Add a title page
    merged_content.append("# Hello-Agents: 动手学智能体\n\n")
    merged_content.append("<div style=\"page-break-after: always;\"></div>\n\n")

    for title, rel_path in links:
        # Ignore external links (starting with http)
        if rel_path.startswith('http'):
            continue
            
        # Unquote URL encoding (e.g., %20 -> space)
        clean_path = unquote(rel_path)
        
        # Resolve path relative to the sidebar file's directory
        if clean_path.startswith('./'):
            clean_path = clean_path[2:]
            
        abs_path = os.path.join(base_dir, clean_path)
        
        if not os.path.exists(abs_path):
            print(f"Warning: File not found: {abs_path}")
            continue
            
        print(f"Merging: {abs_path}")
        
        with open(abs_path, 'r', encoding='utf-8') as f:
            file_content = f.read()
            
            # Add a page break before each file/chapter
            merged_content.append(f"\n\n<!-- PAGE BREAK -->\n<div style=\"page-break-after: always;\"></div>\n\n")
            
            # Append the content
            merged_content.append(file_content)
            merged_content.append("\n\n")

    print(f"Writing merged content to {output_path}...")
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("".join(merged_content))
    
    return True

import json

def convert_to_pdf(input_path):
    # Create temporary HTML file
    html_path = input_path.replace('.md', '.html')
    pdf_path = input_path.replace('.md', '.pdf')
    
    print(f"Step 1: Converting {input_path} to HTML using Pandoc...")
    try:
        subprocess.run(
            ["pandoc", input_path, "-o", html_path],
            check=True
        )
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"Error during Pandoc conversion: {e}")
        # Try fall back to md-to-pdf if pandoc fails (unlikely given verification) or just warn
        print("Ensure 'pandoc' is installed.")
        return False

    print(f"Step 2: Converting HTML to PDF using Chrome Headless...")
    
    # Check for system Chrome on macOS
    system_chrome = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    if not os.path.exists(system_chrome):
        print(f"Error: Google Chrome not found at {system_chrome}")
        return False

    cmd = [
        system_chrome,
        "--headless",
        "--disable-gpu",
        f"--print-to-pdf={pdf_path}",
        f"file://{html_path}"
    ]
    
    try:
        subprocess.run(cmd, check=True)
        print(f"PDF generation successful: {pdf_path}")
        
        # Cleanup HTML
        if os.path.exists(html_path):
            os.remove(html_path)
            
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error during Chrome PDF conversion: {e}")
        return False

if __name__ == "__main__":
    # Get project root (parent of the scripts directory)
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
    
    SIDEBAR_FILE = os.path.join(PROJECT_ROOT, "docs/_sidebar.md")
    DOCS_DIR = os.path.join(PROJECT_ROOT, "docs")
    OUTPUT_MD = os.path.join(PROJECT_ROOT, "docs/Hello-Agents-Full.md")
    
    success = merge_markdown_files(SIDEBAR_FILE, DOCS_DIR, OUTPUT_MD)
    
    if success:
        # Ask or check if PDF conversion is desired
        # For full automation, we just do it.
        convert_to_pdf(OUTPUT_MD)
    else:
        sys.exit(1)
