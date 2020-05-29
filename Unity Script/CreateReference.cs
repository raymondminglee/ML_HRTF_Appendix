using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Oculus.Platform;

public class CreateReference : MonoBehaviour
{
    public Transform Speaker;
    //GameObject Speakerclone;

    // number of azimuth from 1 to 25
    public int azn;
    // number of elevation from 1 to 50
    public int eln;
    // raduis
    public int r;

    // create 

    int c = 0;

    // for height 
    public int height;

    // Use this for initialization

    float[] elevation = new float[50];

    void Start()
    {
        for (int i = 0; i <= eln; i++)
        {
            elevation[i] = -45 + 135 * (float)i/eln ;
            Debug.Log(elevation[i]);
        }

        // instantiate new game object speaker
        for (int j = 0; j <= azn; j++)
        {
            int azimuth = -80 + j * (160/azn);
            for (int k = 0; k <= eln; k++)
            {
                float X_1 = r * Mathf.Sin(azimuth * Mathf.PI / 180);
                float X_2 = r * Mathf.Cos(azimuth * Mathf.PI / 180) * Mathf.Cos(elevation[k] * Mathf.PI / 180);
                float X_3 = r * Mathf.Cos(azimuth * Mathf.PI / 180) * Mathf.Sin(elevation[k] * Mathf.PI / 180) + height;
                //Speakerclone = Instantiate(Speaker, new Vector3(X_1, X_3, X_2), Quaternion.identity) as GameObject;
                Instantiate(Speaker, new Vector3(X_1, X_3, X_2), Quaternion.identity);
            }
        }
    }

    // Update is called once per frame




    /*
        private void OnGUI()
        {
            if(GUI.Button(new Rect(20, Screen.height * 0.66f, 200, 30), "Initialize Virtual Speaker"))
            {
                CreateClones();
            }

        }
        */
}
