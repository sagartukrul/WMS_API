using System;
using System.Collections.Generic;
using System.Text;
using System.Runtime.InteropServices;

namespace Scanning.Classes
{
   public static class DeviceError
    {
        [DllImport("CoreDll.dll", EntryPoint = "PlaySound")]
        private static extern int WCE_PlaySound(string szSound, IntPtr hMod, int flags);
        public static void PlaySoundFile(string soundFile)
        {
            //const object SND_ASYNC = 1;
            //const object SND_FILENAME = 131072;
            WCE_PlaySound(soundFile, IntPtr.Zero, 1);
        }
    }
}
