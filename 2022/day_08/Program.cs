using System;
using System.Collections.Generic;
using System.IO;
using System.Text;

namespace advent_of_code_2022
{
    public class day_08
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

            // Console.WriteLine($"Input Path: \"{inputPath}\"");
            List<List<int>> grid = new();
            Load(inputPath, grid);
            // PrintData(grid);

            // Part 1
            Console.WriteLine(Part1(grid));

            // Part 2
            Console.WriteLine(Part2(grid));

            return 0;
        }

        static void Load(String path, List<List<int>> grid)
        {
            foreach(string line in File.ReadAllLines(path))
            {
                String lineTrim  = line.Trim();
                if (lineTrim.Length > 0)
                {
                    List<int> row = new();
                    for (int i = 0; i < lineTrim.Length; ++i)
                    {
                        if (Int32.TryParse(lineTrim.Substring(i, 1), out int item))
                        {
                            row.Add(item);
                        }
                    }
                    grid.Add(row);
                }
            }
        }

        static void PrintData(List<List<int>> grid)
        {
            StringBuilder buff = new StringBuilder();
            bool printNewline = false;
            foreach(List<int> row in grid)
            {
                if (printNewline)
                    buff.Append('\n');
                printNewline = true;

                bool printComma = false;
                foreach(int item in row)
                {
                    if (printComma)
                        buff.Append(",");
                    printComma = true;
                    buff.Append($"{item}");
                }
            }
            Console.WriteLine(buff.ToString());
        }

        static bool IsVisible(List<List<int>> grid, int col, int row)
        {            
            if ((row <= 0) || (row > grid.Count - 2))
                return true;

            if ((col <= 0) || (col > grid[row].Count - 2))
                return true;

            int currentHeight = grid[row][col];

            bool up = true, down = true, left = true, right = true;
            // Probe up
            for(int j = row - 1; j >= 0; --j)
            {
                if (grid[j][col] >= currentHeight)
                {
                    //Console.WriteLine($"grid[{j}][{col}] >= grid[{row}][{col}] visible (U)!");
                    up = false;
                    break;
                }
            }

            // Probe down
            for(int j = row + 1; j < grid.Count; ++j)
            {
                if (grid[j][col] >= currentHeight)
                {
                    //Console.WriteLine($"grid[{j}][{col}] >= grid[{row}][{col}] visible (D)!");
                    down = false;
                    break;
                }
            }

            // Probe left
            for(int i = col - 1; i >= 0; --i)
            {
                if (grid[row][i] >= currentHeight)
                {
                    //Console.WriteLine($"grid[{row}][{i}] >= grid[{row}][{col}] visible (L)!");
                    left = false;
                    break;
                }
            }

            // Probe right
            for(int i = col + 1; i < grid[row].Count; ++i)
            {
                if (grid[row][i] >= currentHeight)
                {
                    //Console.WriteLine($"grid[{row}][{i}] >= grid[{row}][{col}] visible (R)!");
                    right = false;
                    break;
                }
            }

            /*
            if (left || right || up || down)
                Console.WriteLine($"grid[{row}][{col}] = {grid[row][col]} visible! {up},{down},{left},{right}");
            */
            
            return (left || right || up || down);
        }

        static int ScoreLocation(List<List<int>> grid, int col, int row)
        {            
            int currentHeight = grid[row][col];

            int up = 0, down = 0, left = 0, right = 0;
            // Probe up
            if (row  > 0)
            {
                for(int j = row - 1; j >= 0; --j)
                {
                    up++;
                    if (grid[j][col] >= currentHeight)
                        break;                    
                }
            }

            // Probe down
            if (row < grid.Count - 1)
            {
                for(int j = row + 1; j < grid.Count; ++j)
                {
                    down++;
                    if (grid[j][col] >= currentHeight)
                        break;                    
                }
            }

            // Probe left
            if (col > 0)
            {
                for(int i = col - 1; i >= 0; --i)
                {
                    left++;
                    if (grid[row][i] >= currentHeight)
                        break;
                    
                }
            }

            // Probe right
            if (col < grid[row].Count - 1)
            {
                for(int i = col + 1; i < grid[row].Count; ++i)
                {
                    right++;
                    if (grid[row][i] >= currentHeight)
                        break;
                    
                }
            }

            return (left * right * up * down);
        }
        
        static int Part1(List<List<int>> grid)
        {
            int visibleCount = 0;            
            for(int j = 0; j < grid.Count; ++j)
            {
                for(int i = 0; i < grid[j].Count; ++i)
                {
                    if (IsVisible(grid, i, j))
                        visibleCount++;
                }
            }

            return visibleCount;
        }        

        static int Part2(List<List<int>> grid)
        {
            int maxScore = 0;            
            for(int j = 0; j < grid.Count; ++j)
            {
                for(int i = 0; i < grid[j].Count; ++i)
                {
                    int score = ScoreLocation(grid, i, j);
                    if (score > maxScore)
                        maxScore = score;
                    // Console.WriteLine($"grid[{j}][{i}] = {score} vs. {maxScore}.");
                }
            }

            return maxScore;
        }
    }
}