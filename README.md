# heroku-hook-forwarder
Heroku http deploy hook forward to circle ci API

see .env_template for env variables

* warning * heroku http hook doesn't deliver the branch name, so the lookup for sha1 -> branch name is made manually.
Branch lookup is only suppored for Github public repos for now, PRs welcome for other repos
 
