# Submitting Data to Data Repositories

## NCBI SRA

1. Initiate the SRA submission process on NCBI
2. Fill out all necessary metadata tables/project details
3. At the file upload step, select "FTP Instructions"
4. Run `ftp [ftp link]` where `[ftp link]` is the string it sends you starting with `ftp-`
5. For some reason that eludes me, this fails every time, so just type `quit` and rerun the exact same command as before. This will prompt you for a username. Enter the username it says in the "FTP Instructions" (something like `subftp`)
6. Enter the password from the portal when prompted
7. Enter the directory by copying the `cd` command in the portal
8. Create a new directory (I usually do something like `projectname_datatype`)
9. Change into the new directory
10. Type `mput *.fq.gz` or `mput *.fastq.gz` depending on your file extension
11. It will ask something with mput followed by a bunch of letters. Type `a` and click enter (this means "all" with regards to the files following the wildcard you specified)
12. Run this whole thing in screen, otherwise the transfer will stop once you log out/internet cuts out. When you check in and it says the transfer is complete, log back into the NCBI SRA portal and load the folder you made use "Preload Folder" and it will confirm the files are all uploaded