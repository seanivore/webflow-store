# Resurrect Webflow Site with **HUGE PRINT STORE**

This was started, damaged, and ended up being all we have to work with. 
`/Users/seanivore/Development/webflow-store/`
- The Github Repo is also "webflow-store" 
- Git is set up to "git push" 
- But just FYI Git branch is also "webflow-store" 

The entire repository is now indexed in Cursor for you! 

Once the website is working locally, we will be pushing it to Github Pages/Jekyll. 
- I have already created the _config.yml file for this 
- The CNAME file is already created 

## Notable Issues and Observations

1. The most notable issue is that the ./assets/images/ files had their Webflow ID removed from the file name 
2. The main root pages preview properly; this doesn't mean they are done, for some reason Webflow CDN files will work on pages long after the Webflow site is deleted. But it seems worth noting as a way to check on things as we progress along. 

### PREVIEWING PROPERLY: 
   - /Users/seanivore/Development/webflow-store/index.html 
   - /Users/seanivore/Development/webflow-store/legal-privacy-terms.html
   - /Users/seanivore/Development/webflow-store/contact.html
   - /Users/seanivore/Development/webflow-store/about.html

### PAGES IN THESE DIRECTORIES PREVIEW WITHOUT CSS: 
   - /Users/seanivore/Development/webflow-store/fashion/lookbook/* 
   - /Users/seanivore/Development/webflow-store/understand-trends/buy-historic-artwork/original-print-series/*
   - /Users/seanivore/Development/webflow-store/understand-trends/buy-historic-artwork/original-single-edition-prints/*
   - /Users/seanivore/Development/webflow-store/understand-trends/buy-historic-artwork/shop-prints-by-aesthetic/*

### Of those pages, these two are are important. 
1. The first is just one page for the store that filters and sorts all the prints. 
2. The second is the first page of the lookbook. 

  > The very important print store does not have CSS applied: 
    > file:///Users/seanivore/Development/webflow-store/art-movement-museum/buy-historic-prints.html
        - This was a very complex page that sorted using many different CMS Collection "tags" 
        - There are over 500+ prints in the store 

I THINK THE REST OF THE PAGES IN THAT DIRECTORY ARE SO SIMILAR LOOKING BECAUSE OF PAGINATION. 
- /Users/seanivore/Development/webflow-store/art-movement-museum/*

  > The very important lookbook does not have CSS applied: 
    > file:///Users/seanivore/Development/webflow-store/fashion/lookbook/summer-2024-cover.html
        - We have the other one so we need this one too it 
        - Shouldn't be as crazy to fix as the store, but still a bunch of pages that pull from various CMS collections 

## Objective 

I would like to be as pragmatic as possible: 
  1. Review the entire codebase and HTML files to see what the various state of the paths and URLs are 
  2. Make notes of these observations so that when planning, one fix won't break something else 
  3. Note that the slug of the images will need to be used to connect to more of the image URLs 
  4. Create a plan, with phases, that we can stay grounded and follow

My hope is that this way you can use all your crazy python script writing fixes, but without giving me that 'chicken running around with their head cut off' feeling. This hopefully will also help you avoid accidentally getting stuck into looping and compounding troubleshooting issues. That is what happened the first time we tried to fix this BUT that was a long time ago now and we've learned a lot since then. 
