using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Text.RegularExpressions;

namespace advent_of_code_2022
{

    public class Point
    {
        public int x {get; set;}
        public int y {get; set;}

        public Point()
        {
            x = 0;
            y = 0;            
        }

        public Point(int x, int y)
        {
            this.x = x;
            this.y = y;
        }

        public override string ToString()
        {
            return $"({x},{y})";
        }

        public override bool Equals(object? obj)
        {
            if (obj == null)
                return false;
            else if (obj is Point)
            {
                return ((Point)obj).x == x && ((Point)obj).y == y;
            }
            else
            {
                return false;
            }
        }

        public override int GetHashCode()
        {
            
            return (y << 16) + x;
        }
    }

    public class day_14
    {
        public static int Main(string[] args)
        {
            string inputPath = "sample_input.txt";
            if (args.Length > 0)
            {
                inputPath = args[0];
            }

            if (!File.Exists(inputPath))
            {
                Console.WriteLine($"Error: File Not Found \"{inputPath}\"");
                return -1;
            }

            Dictionary<Point, char> data = Load(inputPath);            
            //PrintData(data);

            // Part 1
            Console.WriteLine(Part1(data));

            // Part 2
            Console.WriteLine(Part2(data));

            return 0;
        }

        static Dictionary<Point, char> Load(String path)
        {
            Dictionary<Point, char> data = new();
            Regex readPoint = new Regex(@"(?'x'\d+),(?'y'\d+)", RegexOptions.Compiled);
            int lineNum = 0;

            foreach(String row in File.ReadAllLines(path))
            {
                lineNum++;
                String line = row.Trim();
                if (line.Length > 0)
                {
                    bool firstPoint = true;
                    int x1 = 0, y1 = 0, x2 = 0, y2 = 0;   
                    if (readPoint.IsMatch(line))
                    {
                        MatchCollection matches = readPoint.Matches(line);
                        foreach(Match match in matches)
                        {
                            GroupCollection groups = match.Groups;    
                            if (!Int32.TryParse(groups["x"].Value, out int x))
                            {
                                Console.WriteLine($"Error Parsing Point.x for line #{lineNum}: {line}.");
                                break;
                            }
                            if (!Int32.TryParse(groups["y"].Value, out int y))
                            {
                                Console.WriteLine($"Error Parsing Point.y for line #{lineNum}: {line}.");
                                break;
                            }
                            x1 = x2;
                            y1 = y2;
                            x2 = x;
                            y2 = y;
                            if (!firstPoint)
                            {
                                if (x1 == x2) 
                                {
                                    // vertical line.
                                    int a = Math.Min(y1, y2);
                                    int b = Math.Max(y1, y2);
                                    for(int j = a; j <= b; ++j)
                                    {
                                        data[new Point(x1, j)] = '#';
                                    }
                                }
                                else 
                                {
                                    // horizontal line
                                    int a = Math.Min(x1, x2);
                                    int b = Math.Max(x1, x2);
                                    for(int i = a; i <= b; ++i)
                                    {
                                        data[new Point(i, y1)] = '#';
                                    }
                                }
                            }
                            firstPoint = false;
                        } // match
                    } // is match?
                } // line not empty.
            } // row in input
            return data;
        }

        static void Bounds(Dictionary<Point, char> data, ref int minX, ref int minY, ref int maxX, ref int maxY)
        {
            minX = Int32.MaxValue;
            minY = Int32.MaxValue;
            maxX = Int32.MinValue;
            maxY = Int32.MinValue;

            foreach(Point p in data.Keys)
            {
                minX = Math.Min(minX, p.x);
                minY = Math.Min(minY, p.y);
                maxX = Math.Max(maxX, p.x);
                maxY = Math.Max(maxY, p.y);
            }
        }

        static void PrintData(Dictionary<Point, char> data)
        {
            int minX = Int32.MaxValue;
            int minY = Int32.MaxValue;
            int maxX = Int32.MinValue;
            int maxY = Int32.MinValue;

            Bounds(data, ref minX, ref minY, ref maxX, ref maxY);
            Point p0 = new Point(502, 9);
            Point p1 = new Point(502, 9);

            for (int y = minY; y <= maxY; ++ y)
            {
                for(int x = minX; x <= maxX; ++x)
                {
                    Point pt = new Point(x, y);
                    Console.Write(data.GetValueOrDefault(pt, '.'));
                }
                Console.WriteLine("");
            }
            Console.WriteLine("");
        }

        static bool Simulate1(Dictionary<Point, char> data, int dropX, int dropY, int minY, int maxY)
        {            
            Point sand = new Point(dropX, dropY);
            bool done = false;
            int x = dropX;
            int y = dropY;

            while (!done)
            {
                if (!data.ContainsKey(new Point(x, y + 1)))
                {
                    // Fall one square down
                    y++;

                }
                else if (!data.ContainsKey(new Point(x - 1, y + 1)))
                {
                    // Fall to left diagonally.
                    x--;
                    y++;

                }
                else if (!data.ContainsKey(new Point(x + 1, y + 1)))
                {
                    // Fall to right diagonally.
                    x++;
                    y++;
                }
                else 
                {
                    // Cannot move come to rest.
                    data[new Point(x, y)] = 'o';
                    done = true;
                }

                if ((y < minY) || (y > maxY))
                    done = true; // done if out of bounds.
            }

            return ((y < minY) || (y > maxY)); // Continue as long as in bounds.
        }

        static bool Simulate2(Dictionary<Point, char> data, Point dropPoint, int floorY)
        {                        
            int x = dropPoint.x;
            int y = dropPoint.y;
            Point sand = new Point(x, y);

            bool done = data.GetValueOrDefault(dropPoint, '.') != '.';

            while (!done)
            {
                if (!data.ContainsKey(new Point(x, y + 1)) && (y < floorY - 1))
                {
                    // Fall one square down
                    y++;

                }
                else if (!data.ContainsKey(new Point(x - 1, y + 1)) && (y < floorY - 1))
                {
                    // Fall to left diagonally.
                    x--;
                    y++;

                }
                else if (!data.ContainsKey(new Point(x + 1, y + 1)) && (y < floorY - 1))
                {
                    // Fall to right diagonally.
                    x++;
                    y++;
                }
                else 
                {
                    // Cannot move come to rest.
                    data[new Point(x, y)] = 'o';
                    done = true;
                }
            }
            
            return (data.GetValueOrDefault(dropPoint, '.') != '.'); // Continue as long as hasn't filled the drop point.
        }

        static int Part1(Dictionary<Point, char> data)
        {
            int minX = Int32.MaxValue;
            int minY = Int32.MaxValue;
            int maxX = Int32.MinValue;
            int maxY = Int32.MinValue;

            RemoveSand(data);
            Bounds(data, ref minX, ref minY, ref maxX, ref maxY);
            bool done = false;
            while (!done)
            {
                done = Simulate1(data, 500, 0, -100, maxY + 5);
            }
            // PrintData(data);
            return CountSand(data);
        }

        static int Part2(Dictionary<Point, char> data)
        {
            int minX = Int32.MaxValue;
            int minY = Int32.MaxValue;
            int maxX = Int32.MinValue;
            int maxY = Int32.MinValue;

            RemoveSand(data);
            Bounds(data, ref minX, ref minY, ref maxX, ref maxY);
            Point dropPoint = new Point(500, 0);

            bool done = false;
            while (!done)
            {
                done = Simulate2(data, dropPoint, maxY + 2);
            }
            // PrintData(data);
            return CountSand(data);
 
        }

        static int CountSand(Dictionary<Point, char> data)
        {
            int ret = 0;
            foreach(Point p in data.Keys)
            {
                if (data[p] == 'o')
                {
                    ret++;
                }
            }
            return ret;
        }

        static void RemoveSand(Dictionary<Point, char> data)
        {
            foreach(Point p in data.Keys)
            {
                if (data[p] == 'o')
                {
                    data.Remove(p);
                }
            }
        }
    }
}