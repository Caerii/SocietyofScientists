from setuptools import setup, find_packages

# Read the main README for long description
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='societyofscientists',
    version='0.1.0',
    author='Society of Scientists Team',
    description='A multi-agent AI system for collaborative research grant proposal generation',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(exclude=['tests', 'docs', 'examples', '*.old']),
    install_requires=[
        'ag2[openai]>=0.10.0',  # AG2 (recommended) - active fork, matches your API
        # 'autogen>=0.2.28',  # Microsoft AutoGen (fallback) - old API
        # 'autogen-agentchat>=0.7.0',  # Microsoft AutoGen (fallback) - new API
        'ai21',
        'exa-py',
        'panel',
        'fpdf',
        'markdown',
        'python-dotenv',
    ],
    python_requires='>=3.10',
    include_package_data=True,
    package_data={
        'society_of_scientists': [
            'data/.gitkeep',
            'agent_list.py',
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
    ],
    keywords='multi-agent ai autogen grant-writing research collaboration',
    project_urls={
        'Bug Reports': 'https://github.com/yourusername/SocietyofScientists/issues',
        'Source': 'https://github.com/yourusername/SocietyofScientists',
        'Documentation': 'https://github.com/yourusername/SocietyofScientists/tree/main/docs',
    },
)
