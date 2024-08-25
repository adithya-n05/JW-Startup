import pandas as pd

data = {
    'Name': [
        'Jeff Wilson (LinkedIn)',
        'Jeff Wilson (Capbase)',
        'Jeff Wilson (The Org)',
        'Jeff Wilson (Join Hampton)',
        'Jeff Wilson (Twitter)',
        'Jeff Wilson (YouTube)'
    ],
    'Source': [
        'https://www.linkedin.com/in/jeffwilsonphd/',
        'https://capbase.com/jeff-wilson-minimalistic-design-affordable-housing/',
        'https://theorg.com/org/jupe/org-chart/jeff-wilson-1',
        'https://joinhampton.com/blog/jupe-scaled-to-12-million-in-3-years-with-an-innovative-glamping-tent-and-business-model',
        'https://x.com/ProfDumpster',
        'https://www.youtube.com/watch?v=xN_og8z5yQw'
    ],
    'Description': [
        'Professional profile on LinkedIn.',
        'Article on minimalistic design and affordable housing.',
        'Profile at The Org, CEO/Cofounder at Jupe.',
        'Blog post about scaling Jupe.',
        'Twitter profile.',
        'YouTube video featuring Jeff Wilson.'
    ]
}

df = pd.DataFrame(data)

file_name = 'Jeff_Wilson_Sources.xlsx'
df.to_excel(file_name, index=False)