// Extract the converter RSA key from a KNX signing assembly by reflection.
// Usage: <runtime> _extract.exe <path-to-Knx.Ets.XmlSigning.dll>
// Prints three base64 lines to stdout: MOD=<modulus> EXP=<publicExponent> D=<privateExponent>.
// Runs under .NET (CoreCLR, macOS/Linux/Windows) or Mono or .NET Framework — any runtime that
// provides RSACryptoServiceProvider. .NET/CoreCLR loads obfuscated ETS assemblies that Mono rejects.
// Based on the approach of OpenKNXproducer (https://github.com/OpenKNX/OpenKNXproducer).
using System;
using System.Reflection;
using System.Security.Cryptography;

class Extract
{
    // A static, zero-argument method/property-getter returning an RSA-ish type — the converter key
    // accessor. Guarded so a member whose signature references an unavailable assembly is skipped
    // (some ETS builds reference System.Security.Cryptography.Xml).
    static bool IsKeyAccessor(MethodInfo m)
    {
        try
        {
            return m.GetParameters().Length == 0
                && typeof(AsymmetricAlgorithm).IsAssignableFrom(m.ReturnType);
        }
        catch
        {
            return false;
        }
    }

    static int Main(string[] args)
    {
        if (args.Length < 1)
        {
            Console.Error.WriteLine("usage: _extract.exe <Knx.Ets.XmlSigning.dll>");
            return 2;
        }
        try
        {
            Assembly asm = Assembly.LoadFrom(args[0]);
            Type t = asm.GetType("Knx.Ets.XmlSigning.XmlSigning");
            if (t == null)
            {
                Console.Error.WriteLine("type Knx.Ets.XmlSigning.XmlSigning not found");
                return 3;
            }
            const BindingFlags flags =
                BindingFlags.NonPublic | BindingFlags.Public | BindingFlags.Static;
            // ETS6 exposes GetConverterRsaKey(); obfuscated builds (e.g. ETS5.7) rename it, so fall
            // back to the first static, zero-arg accessor returning an RSA key.
            MethodInfo m = null;
            try { m = t.GetMethod("GetConverterRsaKey", flags); }
            catch { }
            if (m == null)
            {
                foreach (MethodInfo mm in t.GetMethods(flags))
                {
                    if (IsKeyAccessor(mm)) { m = mm; break; }
                }
            }
            if (m == null)
            {
                Console.Error.WriteLine("no converter-key accessor found");
                return 4;
            }
            RSA rsa = (RSA)m.Invoke(null, null);
            RSAParameters p = rsa.ExportParameters(true);
            Console.WriteLine("MOD=" + Convert.ToBase64String(p.Modulus));
            Console.WriteLine("EXP=" + Convert.ToBase64String(p.Exponent));
            Console.WriteLine("D=" + Convert.ToBase64String(p.D));
            return 0;
        }
        catch (Exception e)
        {
            Console.Error.WriteLine("ERR: " + e);
            return 1;
        }
    }
}
