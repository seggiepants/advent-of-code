using System;
using System.Collections.Generic;
using System.IO;
using System.Text.RegularExpressions;

namespace advent_of_code_2022
{
    public class day_07
    {
        public static int Main(string[] args)
        {
            string inputPath = "input.txt";
            if (args.Length > 0)
            {
                inputPath = args[0];
            }

            if (!File.Exists(inputPath))
            {
                Console.WriteLine($"Error: File Not Found \"{inputPath}\"");
                return -1;
            }

            FolderNode root = new FolderNode(null,@"/");
            Load(inputPath, root);
            // PrintData(root);

            // Part 1
            Console.WriteLine(Part1(root));

            // Part 2
            Console.WriteLine(Part2(root));
            
            return 0;
        }


        static void Load(string path, FolderNode root)
        {
            Regex cd = new Regex(@"\$ cd (?'path'.+)", RegexOptions.Compiled);
            Regex ls = new Regex(@"\$ ls", RegexOptions.Compiled);
            Regex fileLine = new Regex(@"(?'size'\d+) (?'name'.+)", RegexOptions.Compiled);
            Regex folderLine = new Regex(@"dir (?'name'.+)", RegexOptions.Compiled);

            FolderNode current = root;

            int lineNum = 0;
            foreach(String row in File.ReadAllLines(path))
            {
                lineNum++;
                String line = row.Trim();
                if (cd.IsMatch(line))
                {
                    MatchCollection matches = cd.Matches(line);
                    foreach(Match match in matches)
                    {
                        GroupCollection groups = match.Groups;    
                        string childPath = groups["path"].Value.Trim();
                        if (childPath == @"/")
                        {
                            current = root;
                        }
                        else if (childPath == "..")
                        {
                            if (current.parent != null)
                            {
                                current = current.parent;
                            }
                        }
                        else // enter a sub folder.
                        {
                            bool found = false;
                            foreach(FolderNode subFolder in current.subFolders)
                            {
                                if (subFolder.name.Equals(childPath))
                                {
                                    found = true;
                                    current = subFolder;
                                    break;
                                }
                            }
                            if (!found)
                            {
                                string subFolderNames = String.Join(',', current.subFolders);
                                return;
                            }
                        }
                    }
                }
                else if (ls.IsMatch(line))
                {
                    // Listing of current folder incoming, do nothing.
                }
                else if (folderLine.IsMatch(line))
                {
                    MatchCollection matches = folderLine.Matches(line);
                    foreach(Match match in matches)
                    {
                        GroupCollection groups = match.Groups;    
                        String folderName = groups["name"].Value.Trim();                        
                        bool exists = false;

                        foreach (FolderNode node in current.subFolders)
                        {
                            if (node.name.Equals(folderName))
                            {
                                exists = true;
                                break;
                            }
                        }

                        if (!exists)
                        {
                            current.subFolders.Add(new FolderNode(current, folderName));
                        }
                    }

                }
                else if (fileLine.IsMatch(line))
                {
                    MatchCollection matches = fileLine.Matches(line);
                    foreach(Match match in matches)
                    {
                        GroupCollection groups = match.Groups;    
                        String name = groups["name"].Value.Trim();
                        if (!Int32.TryParse(groups["size"].Value, out int size))
                        {
                            Console.WriteLine($"Error Parsing file size for {line}.");
                            return;
                        }
                        bool exists = false;
                        foreach (Tuple<String, int> file in current.files)
                        {
                            if (file.Item1.Equals(name))
                            {
                                exists = true;
                                break;
                            }
                        }
                        if (!exists)
                        {
                            current.files.Add(new Tuple<String, int>(name, size));
                        }
                    }
                }
                else
                {
                    Console.WriteLine($"No Match: {line}");
                }
            }
 
        }

        static void PrintData(FolderNode root)
        {
            Console.WriteLine(root.name);
            PrintData_Helper(root, 0);
        }

        static void PrintData_Helper(FolderNode node, int indent)
        {
            foreach(Tuple<String, int>file in node.files)
            {
                Console.WriteLine(new String(' ', indent * 3) + $"- {file.Item2}\t{file.Item1}");
            }
            foreach(FolderNode fldr in node.subFolders)
            {
                Console.WriteLine(new String(' ', indent * 3) + $"- {fldr.name}");
                PrintData_Helper(fldr, indent + 1);
            }
        }

        static String Part1(FolderNode root)
        {
            return Part1_Helper(root, 100000).ToString();
        }        

        static int Part1_Helper(FolderNode root, int maxSize)
        {
            int result = 0;
            int folderSize = root.size;
            if (folderSize < maxSize)
                result += folderSize;
            
            foreach(FolderNode subFolder in root.subFolders)
            {
                result += Part1_Helper(subFolder, maxSize);
            }
            return result;
        }

        static int Part2(FolderNode root)
        {
            const int driveSize = 70000000;
            const int freeSpaceRequired = 30000000;
            int rootSize = root.size;
            int unusedSize = driveSize - rootSize;
            int spaceToFree = freeSpaceRequired - unusedSize;

            
            return Part2_Helper(root, spaceToFree, rootSize);
        }

        static int Part2_Helper(FolderNode root, int spaceToFree, int currentBest)
        {
            int ret = currentBest;
            int folderSize = root.size;
            if ((folderSize >= spaceToFree) && (folderSize < ret))
                ret = folderSize;

            foreach(FolderNode subFolder in root.subFolders)
            {
                int candidate = Part2_Helper(subFolder, spaceToFree, ret);
                if ((candidate >= spaceToFree) && (candidate < ret))
                    ret = candidate;
            }
            return ret;
        }
    }

    public class FolderNode
    {
        public FolderNode? parent;
        public String name;
        public List<Tuple<String, int>> files;
        public List<FolderNode> subFolders;

        public FolderNode(FolderNode? parent, string name)
        {
            this.parent = parent;
            this.name = name;
            files = new();
            subFolders = new();
        }

        public override String ToString()
        {
            return name;
        }

        public int size {
            get {
                int sum = 0;
                foreach(Tuple<String, int>file in files)
                {
                    sum += file.Item2;
                }

                foreach(FolderNode subFolder in subFolders)
                {
                    sum += subFolder.size;
                }
                return sum;
            }
        }
    }
}