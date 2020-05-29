/************************************************************************************

Copyright   :   Copyright 2017-Present Oculus VR, LLC. All Rights reserved.

Licensed under the Oculus VR Rift SDK License Version 3.2 (the "License");
you may not use the Oculus VR Rift SDK except in compliance with the License,
which is provided at the time of installation or download, or which
otherwise accompanies this software in either electronic or hard copy form.

You may obtain a copy of the License at

http://www.oculusvr.com/licenses/LICENSE-3.2

Unless required by applicable law or agreed to in writing, the Oculus VR SDK
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

************************************************************************************/

using System;
using System.IO;
using UnityEngine;
using UnityEngine.VR;
using UnityEngine.SceneManagement;


public class Tutorial : MonoBehaviour
{
    protected Material oldHoverMat;
    static int trial_num = 0;
    private int ispush;
    public Material yellowMat;
    public Material blueMat;
    public Material Next_idle;
    public Material Next_active;
    public Material Play_idle;
    public Material Play_active;
    public Material Finish_idle;
    public Material Finish_active;
    public GameObject Play_button;
    public GameObject Next_button;
    public GameObject Finish_button;
    public GameObject EyeCenter;
    private AudioSource stimuli;
    private bool Next_button_activity = false;
    String[] stimuli_name = new string[] { "training_1", "training_2", "training_3", "training_4", "training_5" };


    void Start()
    {
        ispush = 0;
        Next_button.SetActive(false);
        Finish_button.SetActive(false);
        if (trial_num == stimuli_name.Length)
        {
            Play_button.SetActive(false);
            Next_button.SetActive(false);
            Finish_button.SetActive(true);
        }
    }

    public void OnHoverEnter(Transform t)
    {
        if (t.gameObject.name == "Next_button")
        {
            t.gameObject.GetComponent<Renderer>().material = Next_active;
        }
        if (t.gameObject.name == "Play_button")
        {
            t.gameObject.GetComponent<Renderer>().material = Play_active;
        }
        if (t.gameObject.name == "Speaker" || t.gameObject.name == "Speaker(Clone)")
        {
            oldHoverMat = t.gameObject.GetComponent<Renderer>().material;
            t.gameObject.GetComponent<Renderer>().material = yellowMat;
        }
        if (t.gameObject.name == "Finish_button")
        {
            t.gameObject.GetComponent<Renderer>().material = Finish_active;
        }

    }

    public void OnHoverExit(Transform t)
    {
        if (t.gameObject.name == "Next_button")
        {
            t.gameObject.GetComponent<Renderer>().material = Next_idle;
        }
        if (t.gameObject.name == "Play_button")
        {
            t.gameObject.GetComponent<Renderer>().material = Play_idle;
        }
        if (t.gameObject.name == "Speaker" || t.gameObject.name == "Speaker(Clone)")
        {
            t.gameObject.GetComponent<Renderer>().material = oldHoverMat;
        }
        if (t.gameObject.name == "Finish_button")
        {
            t.gameObject.GetComponent<Renderer>().material = Finish_idle;
        }
    }


    public void OnSelected(Transform t)
    {
        if (t.gameObject.name == "Next_button")
        {
            trial_num += 1;
            //print(trial_num);
            SceneManager.LoadScene(SceneManager.GetActiveScene().name);
            print(trial_num);
            // refreash
        }
        if (t.gameObject.name == "Play_button")
        {
            Play_button.SetActive(false);
            Next_button.SetActive(false);
            //string audio_path = Application.dataPath + "/Log_Sub_" + Subjectnum + ".txt";
            stimuli = GetComponent<AudioSource>();
            stimuli.clip = Resources.Load<AudioClip>(stimuli_name[trial_num]);
            //stimuli.clip = 
            print("playing");
            stimuli.Play();
            // play audio here 

        }
        if (t.gameObject.name == "Speaker" || t.gameObject.name == "Speaker(Clone)")
        {
            t.gameObject.GetComponent<Renderer>().material = blueMat;
        }
        if (t.gameObject.name == "Finish_button")
        {
            SceneManager.LoadScene("Lobby", LoadSceneMode.Single);
        }
    }

    void Update(){

        // angles = InputTracking.GetNodeStates(UnityEngine.XRNode.CenterEye);
        if (OVRInput.Get(OVRInput.Button.Two) == true && Next_button.activeSelf == true)
        {
            SceneManager.LoadScene(SceneManager.GetActiveScene().name);
            print(trial_num);
        }
        if (trial_num < stimuli_name.Length){
            if (OVRInput.Get(OVRInput.Button.PrimaryIndexTrigger) == true && ispush == 0 &&
            Play_button.activeSelf == false && Next_button.activeSelf == false){
                    ispush = 1;
                    print(ispush);
                    Debug.Log("Button One Pressed");
                }
                if (OVRInput.Get(OVRInput.Button.One) == true && ispush == 0 &&
                Play_button.activeSelf == false && Next_button.activeSelf == false){
                    stimuli = GetComponent<AudioSource>();
                    stimuli.clip = Resources.Load<AudioClip>(stimuli_name[trial_num]);
                    stimuli.Play();
                    Debug.Log("Button One Pressed");
                }
                if (OVRInput.Get(OVRInput.Button.PrimaryIndexTrigger) == false && ispush == 1){
                    ispush = 0;
                    print(ispush);
                    print(trial_num);
                    Next_button.SetActive(true);
                }
                
        }
        

    }

}
