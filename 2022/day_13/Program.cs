using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Text.RegularExpressions;

namespace advent_of_code_2022
{

    public class Node
    {
        public bool isInt {get; set;}
        public int value {get; set;}
        public List<Node> listValue {get; set;}

        public Node()
        {
            isInt = true;
            value = 0;
            listValue = new List<Node>();
        }

        public override string ToString()
        {
            StringBuilder sb = new();

            if (isInt)
            {
                sb.Append(value);
            }
            else
            {
                sb.Append("[");
                bool showComma = false;
                foreach(Node node in listValue)
                {
                    if (showComma)
                        sb.Append(", ");
                    showComma = true;
                    sb.Append(node.ToString());
                }
                sb.Append("]");
            }

            return sb.ToString();
        }

        // Returns 
        // -1 if left < right
        // 0 if left == right
        // 1 if left > right
        public static int Compare(Node left, Node right)
        {
            if (left.isInt && right.isInt)
            {
                if (left.value == right.value)
                    return 0;
                else if (left.value < right.value)
                    return -1;
                else
                    return 1; // left.value > right.value;
            }
            else
            {
                // Two lists or a mix of int and list. If int upgrade to list.
                Node a;
                Node b;
                if (left.isInt)
                {
                    a = new Node();
                    a.isInt = false;
                    Node a1 = new Node();
                    a1.isInt = true;
                    a1.value = left.value;
                    a.listValue.Add(a1);
                }
                else
                {
                    a = left;
                }

                if (right.isInt)
                {
                    b = new Node();
                    b.isInt = false;
                    Node b1 = new Node();
                    b1.isInt = true;
                    b1.value = right.value;
                    b.listValue.Add(b1);
                }
                else
                {
                    b = right;
                }
                
                bool done = false;
                int i = 0;
                int ret = 0;
                while (!done)
                {
                    if ((i >= a.listValue.Count) && (i < b.listValue.Count))
                    {
                        // Ran out of left first so smaller.
                        ret = -1;
                        done = true;
                    }
                    else if ((i < a.listValue.Count) && (i >= b.listValue.Count))
                    {
                        // Ran out of right first so smaller.
                        ret =  1;
                        done = true;
                    }
                    else if ((i >= a.listValue.Count) && (i >= b.listValue.Count))
                    {
                        // Ran out of both simultaneously, must be the same.
                        ret = 0;
                        done = true;
                    }
                    else
                    {
                        // Compare item i in both lists.
                        ret = Compare(a.listValue[i], b.listValue[i]);
                    }
                    i++;      
                    if (i >= left.listValue.Count && i >= right.listValue.Count)
                    {
                        done = true;
                    }
                    if (ret != 0)
                        done = true;
                }
                return ret;
            }
            return 0;
        }
    }
    public class day_13
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

            List<Node> data = Load(inputPath);            
            //PrintData(data);

            // Part 1
            Console.WriteLine(Part1(data));

            // Part 2
            Console.WriteLine(Part2(data));

            return 0;
        }

        static List<Node> Load(String path)
        {
            int lineNum = 0;
            List<Node> nodes = new();
            List<Node> nodeStack = new();
            foreach(String row in File.ReadAllLines(path))
            {
                lineNum++;
                String line = row.Trim();
                if (line.Length > 0)
                {   
                    string intText = "";
                    foreach(char c in line)
                    {
                        if (intText.Length > 0 && (c < '0' || c > '9'))
                        {
                            // Write out the int.
                            if (int.TryParse(intText, out int num))
                            {
                                Node parent;
                                if (nodeStack.Count > 0)
                                    parent = nodeStack[nodeStack.Count - 1];
                                else
                                {
                                    Console.WriteLine($"Nothing on the stack for '{c}' intText = \"{intText}\" in \"{line}\".");
                                    return nodes;
                                }
                                Node intNode = new Node();
                                intNode.isInt = true;
                                intNode.value = num;
                                parent.listValue.Add(intNode);
                            }
                            intText = "";                            
                        }

                        if (c == '[')
                        {
                            // Start a list.
                            
                            // Start a new node of type list.
                            Node current = new Node();
                            current.isInt = false;
                            if (nodeStack.Count == 0)
                            {
                                nodeStack.Add(current);
                                nodes.Add(current);
                            }
                            else
                            {
                                Node parent = nodeStack[nodeStack.Count - 1];
                                parent.listValue.Add(current); // Add to current item on top of the stack.
                                nodeStack.Add(current); // Push self to top of stack.
                            }
                        }
                        else if (c == ']')
                        {
                            // End the current list.
                            // just pop the top of the stack.
                            nodeStack.RemoveAt(nodeStack.Count - 1);
                        }
                        else if (c >= '0' && c <= '9')
                        {
                            intText += c;
                        }
                    }

                    // Last part of line may have an int in progress
                    if (intText.Length > 0)
                    {
                        // Write out the int.
                        if (int.TryParse(intText, out int num))
                        {
                            Node parent = nodeStack[nodeStack.Count - 1];
                            Node intNode = new Node();
                            intNode.isInt = true;
                            intNode.value = num;
                            parent.listValue.Add(intNode);
                        }
                        intText = "";                            
                    }
                }
            }
            return nodes;
        }

        static void PrintData(List<Node> data)
        {
            foreach(Node node in data)
            {
                Console.WriteLine(node.ToString());
            }
        }


        static int Part1(List<Node> data)
        {
            int total = 0;
            int index = 1;
            for(int i = 0; i < data.Count; i+=2)
            {
                Node a = data[i];
                Node b = data[i + 1];
                if (Node.Compare(a, b) <= 0)
                {
                    total += index;
                }
                index++;
            }
            return total;
        }

        static int Part2(List<Node> data)
        {   
            List<Node> sortedNodes = new();
            foreach(Node node in data)
            {
                sortedNodes.Add(node);
            }

            Node divider2 = MakeDivider(2);
            Node divider6 = MakeDivider(6);
            sortedNodes.Add(divider2);
            sortedNodes.Add(divider6);
            
            sortedNodes.Sort(Node.Compare);
            int idx2 = 0;
            int idx6 = 0;
            int index = 0;
            foreach(Node node in sortedNodes)
            {
                index++;

                if (Node.Compare(node,divider2) == 0)
                    idx2 = index;
                else if (Node.Compare(node, divider6) == 0)
                    idx6 = index;
            }
            return idx2 * idx6;
        }

        static Node MakeDivider(int num)
        {
            Node divider = new Node();
            divider.isInt = false;
            Node tempList = new Node();
            tempList.isInt = false;
            Node tempNum = new Node();
            tempNum.isInt = true;
            tempNum.value = num;
            tempList.listValue.Add(tempNum);
            divider.listValue.Add(tempList);

            return divider;
        }
    }
}