# Animation Annotator

Code to run and host the annotator. To use make sure you have label-studio v0.9.0.post5 (any version before v1.0 should work).

Once the animations are generated, run the following command to set up the annotator:

`label-studio start whale_annotator --init -b --label-config config.xml --input-path=**PATH ON THE MACHINE TO TASK JSONS**/task_jsons --input-format=json-dir --username=whalebehavior --password=spermwhales21`

Make sure that the `task_jsons` directory (which has all the animation json files in it) is in the same directory that you run this command in. 

Once the command has run, kill the command (Ctrl + C).

Next, move the `upload` directory (where all the animations are) into the newly created `whale_annotator` directory. 

Finally, run the following command (same as above but no --init):

`label-studio start whale_annotator -b --label-config config.xml --input-path=**PATH ON THE MACHINE TO TASK JSONS**/task_jsons --input-format=json-dir --username=whalebehavior --password=spermwhales21`

Anyone can then visit the annotator to use it by navigating to:

`**YOUR MAcHINE NAME**:8080`

And entering the username: whalebehavior, and password: spermwhales21.
