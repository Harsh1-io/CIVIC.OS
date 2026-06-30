https://docs.google.com/document/d/1TWJBnEDNNi2CdJNd5d-dubHVg3igdasw7oSSH4yES0M/edit?usp=drivesdk

 CIVIC.OS — Real-Time Civic Infrastructure Reporting Platform                                              
                                                                                                          
  Pitch: A fully deployed, end-to-end civic tech platform that turns a citizen's smartphone photo into a    
  categorised, geocoded, map-pinned infrastructure report in under 30 seconds — and gives municipal         
  operators a live analytics layer to see where the city is breaking down before it becomes a crisis. Built 
  from scratch through AI-assisted development using Claude Code, with every component — backend, frontend,
  maps, analytics, auth, and deployment config — generated and iterated through natural language prompts and
   shipped live.                                                                                          
                                                                                                            
  ---                                                                                                       
  The problem                                                                                               
                                              
  Urban infrastructure fails slowly, then all at once. A pothole ignored for six weeks becomes a blown tyre
  and a liability claim. A slow pipe leak becomes a sinkhole. Overflowing bins become a public health
  citation. The breakdown is rarely the infrastructure itself — it is the reporting gap between citizens who
   see problems daily and the systems that are supposed to fix them.
                                                                                                            
  Existing civic reporting tools fail on both ends. Citizens face high-friction forms with too many fields,
  unclear categories, and no feedback that anything happened. Municipal teams receive unstructured data —   
  free-text descriptions, no coordinates, no photos — that requires manual triage before anyone can act. The
   result is a system where most problems go unreported, and the ones that are reported arrive too late or  
  too vague to action efficiently.
                                                                                                            
  CIVIC.OS is built to close that gap entirely.                                                           
                                                                                                          
  ---
  What it does
              
  A citizen opens the app and hits the report button. They photograph the problem — a cracked road, a burst
  pipe, an overflowing skip, a collapsed footpath. An on-device Vision Transformer model (running locally in
   the browser via WebAssembly, no server round-trip) classifies the image into one of four infrastructure
  categories before the citizen has typed a single word. The suggested category appears pre-filled. They can
   keep it or change it. They add a location — either auto-filled from GPS or typed as an address that gets 
  geocoded live against OpenStreetMap — and submit. That's the entire flow.
                                                                                                            
  On the backend, the image is stored on Cloudinary, the report is written to the database with a generated
  short issue ID, and the pin appears on the live map within seconds. The whole process takes under 30    
  seconds from photo to published report.
                                                                                                            
  ---
  The platform                                                                                              
                                                                                                          
  CIVIC.OS is not a form with a map widget. It is a complete operational platform:                        
                                              
  Live Regional Map — every submitted report renders as a category-coloured marker on a dark Leaflet map,
  with real-time filtering by infrastructure type and a full popup on each pin showing the image,
  description, reporter, address, and status. Reports with addresses geocoded to coordinates appear         
  precisely on the map. The map is live — new submissions appear without refresh.                           
                                                                                                            
  Analytics Dashboard — a Chart.js-powered analytics layer showing category breakdown, daily submission     
  volume over the past 14 days, and current resolution rate. Each chart carries configurable threshold lines
   — warning and critical — with automatic alert banners that surface when any category or daily volume   
  breaches safe operating levels. This is the layer that turns raw citizen reports into an ops intelligence 
  feed.
                                                                                                            
  Photo Gallery — a per-category image slideshow with crossfade transitions and a synchronised mini-map   
  panel that pans to each report's pinned location as slides advance. Filterable by category. Auto-plays. 
  Keyboard-navigable. Designed for briefings and situation reviews.
                                                                                                            
  Issue Lifecycle — every report receives a short random human-readable ID (e.g. #K7MQ). Reports move
  through Open → Resolved. Authenticated users can close issues directly from the dashboard with a single   
  click that updates the status in real time without a page reload.                                       
                                                                                                            
  Leaderboard — top reporters ranked with medal tiers, creating a lightweight gamification layer that drives
   sustained citizen participation rather than one-off submissions.                                         
                                                                                                          
  New-Activity Badge — the Gallery nav item displays a pulsing red indicator whenever reports have been     
  filed in the last 24 hours that the user hasn't reviewed, acting as a passive notification system without
  requiring push permissions.                                                                               
                                                                                                          
  Authentication — full JWT-based signup and login with bcrypt password hashing, persistent sessions, and 
  protected endpoints. The report button and close-issue action are auth-gated; the map and analytics are
  public.
                                                                                                            
  ---
  What is actually shipped                                                                                  
                                                                                                          
  Live at https://civic-os.onrender.com — not a mockup, not a localhost demo, a publicly accessible deployed
   application. FastAPI backend on Render's free tier, Cloudinary for image hosting, static frontend served
  from the same process. Auto-deploys on every push to GitHub. The image classification runs client-side in
  WebAssembly — zero inference cost regardless of submission volume.
                                                                                                            
  ---
  Why it matters beyond the demo                                                                            
                                                                                                          
  The in-memory data store is a deliberate architectural decision for the hackathon — the database interface
   is a single file with five async functions. Swapping it for a MongoDB Motor implementation, which is
  already documented in the codebase, adds geospatial indexing for radius queries, compound
  category-and-date indexes for analytics, and change streams for real-time dashboard updates. The platform
  is production-architecture at hackathon speed.                                                            
   
  The on-device inference model means the AI layer is free to scale. There is no per-submission API cost, no
   model hosting bill, no latency from a cloud round-trip. A city of a million residents submitting reports
  simultaneously adds zero marginal AI cost. That is what makes this deployable by a cash-strapped        
  municipality, not just a well-funded startup.                                                             
   
  Built fast, shipped real, solving something that actually matters — and none of it would have existed     
  inside a hackathon window without AI-assisted development. Claude Code handled every file in the stack; 
  the only input was intent.                                                                              
                                            


