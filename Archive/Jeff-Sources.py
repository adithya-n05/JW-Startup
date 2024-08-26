import pandas as pd

data = {
    'Name': [
        'Jeff Wilson (LinkedIn)',
        'Jeff Wilson (Capbase)',
        'Jeff Wilson (The Org)',
        'Jeff Wilson (Join Hampton)',
        'Jeff Wilson (Twitter)',
        'Jeff Wilson (YouTube)',
        'Jeff Wilson (Instagram)',
        'Jeff Wilson (YouTube Interview)',
        'Jeff Wilson (Initialized Blog)',
        'Jeff Wilson (Miami Ad School)',
        'Jeff Wilson (Capital Letter)'
    ],
    'Source': [
        'https://www.linkedin.com/in/jeffwilsonphd/',
        'https://capbase.com/jeff-wilson-minimalistic-design-affordable-housing/',
        'https://theorg.com/org/jupe/org-chart/jeff-wilson-1',
        'https://joinhampton.com/blog/jupe-scaled-to-12-million-in-3-years-with-an-innovative-glamping-tent-and-business-model',
        'https://x.com/ProfDumpster',
        'https://www.youtube.com/watch?v=xN_og8z5yQw',
        'https://www.instagram.com/profdumpster/?hl=am-et',
        'https://www.youtube.com/watch?v=bhuUdCseF3k',
        'https://blog.initialized.com/2022/10/video-interview-with-jeff-wilson-ceo-of-jupe/',
        'https://miamiadschool.com/event/jeff-wilson-jupe/',
        'https://www.capitalletter.com/p/jupe'
    ],
    'Description': [
        'Professional profile on LinkedIn.',
        'Article on minimalistic design and affordable housing.',
        'Profile at The Org, CEO/Cofounder at Jupe.',
        'Blog post about scaling Jupe.',
        'Twitter profile.',
        'YouTube video featuring Jeff Wilson.',
        'Instagram profile.',
        'YouTube interview with Jeff Wilson.',
        'Blog interview with Jeff Wilson, CEO of Jupe.',
        'Event at Miami Ad School featuring Jeff Wilson.',
        'Article on Jupe in Capital Letter.'
    ]
}

df = pd.DataFrame(data)
file_name = 'Jeff_Wilson_Sources.xlsx'
df.to_excel(file_name, index=False)