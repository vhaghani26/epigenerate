# Advanced Configuration

You should have a `.bashrc`, `.profile`, `.bash_profile`, or something of the sort in your home directory. On Epigenerate, since you have a login prompt instead of just SSH key pairs for login, you will need to use `.profile` or `.bash_profile`. I use `.profile` and then just put `source ~/.profile` in the other two files so that if I'm using other SSH features, I still have everything I normally have sourced. Below are some things you can put in your `.profile` to enhance your CLI experience.

## Aliases

After typing `ssh {username}@epigenerate.genomecenter.ucdavis.edu` so many times, you probably want an easier way to do that. You can create an alias! 

```
alias epigenerate='ssh {username}@epigenerate.genomecenter.ucdavis.edu'
```

Then, every time you want to log in, all you need to do is run `epigenerate` and it will prompt you for your password. You can also create your own aliases to easily run commands, change directories, and more.

## Notifications

When you run jobs on SLURM, you get notifications when your job is complete or fails (if you so choose). However, what if you are running a big job on `screen` or `tmux`? Do you just attach to the screen every time you want to check its status? You can, but you can also automate a notification system. Put the following in your `.profile` (or whatever file you use)

```
# Notify function for jobs
notify() {
    DETAILS=$(history | tail -2 | head -1)
    cat <<EOF | sendmail {name}@ucdavis.edu
Subject: done - $*
From: Epigenerate Notification <{name}@epigenerate.ucdavis.edu>

$DETAILS
EOF
}
```

To use the function, you can run:

* `{your command}; notify {email_subject_line}` and it will email you when your command **completes** with the email subject line you gave it
* `{your command} && notify {email_subject_line}` and it will email you if your command **succeeds** with the email subject line you gave it
* `{your command} || notify {email_subject_line}` and it will email you if your command **fails** with the email subject line you gave it

Try running

```
sleep 5; notify test
```

And you will receive an email notification about the job finishing! Read [Titus' explanation](https://hackmd.io/zr2cYCnQQleH2k52i4sgKQ?view) for more information on its usage.

## Changing Command Prompt Colors

Before configuration, almost all text on my screen was white. It made it hard to distinguish the command prompt from the standard error and output. I reset it so that my conda environnment is the default text color, my username and hostname are green, and my working directory is blue. Just put the following in your `.profile` and [adjust the colors](https://dev.to/ifenna__/adding-colors-to-bash-scripts-48g4) if you're interested:

```
# Set color codes
GREEN="\[\e[32m\]"
BLUE="\[\e[36m\]"
RESET_COLOR="\[\e[0m\]"

# Customize the PS1 prompt
PS1="${GREEN}\u@\h${RESET_COLOR}: ${BLUE}\W${RESET_COLOR}\$ "
```

# Viewing CSVs

CSV files are common files for storing data. However, they are not easy on the eye viewing them at the command line. Here is a function called `prettycsv` that allows you to view CSV files easily. Put the following in your `.profile`:

```
prettycsv() {
    if [ -z "$1" ]; then
        echo "Usage: prettycsv [file]"
    else
        cat "$1" | column -t -s, | less -S
    fi
}
```

Now source your `.profile` and test it out on any CSV by running `prettycsv {file.csv}`. For more viewing options and use cases, please visit the [Pretty CSV Website](https://www.stefaanlippens.net/pretty-csv.html).

# Viewing Excel Files

Excel files are binary, making them irritating to quickly check the contents of at the command line. Ensure you have Python and Pandas installed before running this. Add this function to your `.profile`:

```
view_xlsx() {
    python -c "import pandas as pd; print(pd.read_excel('$1').to_csv(index=False))"
}
```

Now you can view Excel files by running:

```
view_xlsx {file.xlsx}
```