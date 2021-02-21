## HOW TO DEPLOY GCF TRIGGERRED BY PUB/SUB

* access to `/source` folder
* run this command
```
gcloud functions --project [project_id] deploy cloudbuild-notifications \
--entry-point cloudbuild_notifications \
--runtime python38 \
--retry \
--env-vars-file ../env.yaml \
--trigger-topic cloud-builds
```