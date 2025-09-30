<<<<<<< HEAD
class SimpleSEOTool:
    def __init__(self):
        self.name = "SEO Optimization Tool"
        self.description = "A tool for optimizing content for search engines by improving keyword placement and SEO structure."

    def _run(self, content: str) -> str:
        try:
            # Extract potential keywords from content
            words = content.lower().split()
            word_count = {}
            for word in words:
                if len(word) > 4:  # Only consider words longer than 4 characters
                    word_count[word] = word_count.get(word, 0) + 1
            
            # Find most common words as potential keywords
            keywords = sorted(word_count.items(), key=lambda x: x[1], reverse=True)[:5]
            
            # Basic SEO improvements
            lines = content.split('\n')
            optimized_lines = []
            
            for line in lines:
                if line.strip():
                    # Add heading structure if not present
                    if not line.startswith('#') and len(line) < 60 and any(kw[0] in line.lower() for kw in keywords):
                        line = f"## {line}"
                    optimized_lines.append(line)
                else:
                    optimized_lines.append(line)
            
            optimized_content = '\n'.join(optimized_lines)
            
            # Add meta description suggestion
            meta_desc = f"Meta Description: {content[:150]}..." if len(content) > 150 else content
            
            return f"{optimized_content}\n\n---\nSEO Suggestions:\n{meta_desc}\nTop Keywords: {', '.join([kw[0] for kw in keywords[:3]])}"
            
        except Exception as e:
            return f"Error optimizing for SEO: {e}"

seo_tool = SimpleSEOTool()
=======
class SimpleSEOTool:
    def __init__(self):
        self.name = "SEO Optimization Tool"
        self.description = "A tool for optimizing content for search engines by improving keyword placement and SEO structure."

    def _run(self, content: str) -> str:
        try:
            # Extract potential keywords from content
            words = content.lower().split()
            word_count = {}
            for word in words:
                if len(word) > 4:  # Only consider words longer than 4 characters
                    word_count[word] = word_count.get(word, 0) + 1
            
            # Find most common words as potential keywords
            keywords = sorted(word_count.items(), key=lambda x: x[1], reverse=True)[:5]
            
            # Basic SEO improvements
            lines = content.split('\n')
            optimized_lines = []
            
            for line in lines:
                if line.strip():
                    # Add heading structure if not present
                    if not line.startswith('#') and len(line) < 60 and any(kw[0] in line.lower() for kw in keywords):
                        line = f"## {line}"
                    optimized_lines.append(line)
                else:
                    optimized_lines.append(line)
            
            optimized_content = '\n'.join(optimized_lines)
            
            # Add meta description suggestion
            meta_desc = f"Meta Description: {content[:150]}..." if len(content) > 150 else content
            
            return f"{optimized_content}\n\n---\nSEO Suggestions:\n{meta_desc}\nTop Keywords: {', '.join([kw[0] for kw in keywords[:3]])}"
            
        except Exception as e:
            return f"Error optimizing for SEO: {e}"

seo_tool = SimpleSEOTool()
>>>>>>> 916d15462f3282d375157da7460c0bb883cb0bcc
