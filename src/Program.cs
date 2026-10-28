using System;
using System.IO;
using System.Security.Cryptography;

byte[] data = new byte[1048576];

RandomNumberGenerator.Fill(data);

File.WriteAllBytes("windows.bin", data);

Console.WriteLine("Random data generated successfully.");
Console.WriteLine("File size: " + data.Length + " bytes");
