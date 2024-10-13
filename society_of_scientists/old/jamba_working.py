from types import SimpleNamespace
from autogen import AssistantAgent, UserProxyAgent
from ai21 import AI21Client
from ai21.models.chat import UserMessage
from types import SimpleNamespace
import autogen
from autogen import AssistantAgent
from autogen.agentchat.contrib.society_of_mind_agent import SocietyOfMindAgent
# import panel as pn
# import asyncio

config_list_custom = [
   {
       "model": "jamba-1.5-large",
       "model_client_cls": "AI21JambaModelClient",
       "api_key": "5AweiGc6E9UDXMCwtYDVhS5y6LarJoLl",
       "temperature": 0.1,
       "top_p": 1.0,
       "max_tokens": 2048
   }
]

class AI21JambaModelClient:
   def __init__(self, config, **kwargs):
       self.api_key = "5AweiGc6E9UDXMCwtYDVhS5y6LarJoLl"
       self.client = AI21Client(api_key=self.api_key)
       self.model = "jamba-1.5-large"
       self.temperature = config.get('temperature', 0.7)
       self.top_p = config.get('top_p', 1.0)
       print(f"AI21JambaModelClient initialized with config: {config}")


   def create(self, params):
       messages = [
           UserMessage(
               content=params["messages"][0]['content']  # Assuming single user message
           )
       ]
      
       # Calling AI21's Jamba API
       response = self.client.chat.completions.create(
           model=self.model,
           messages=messages,
           temperature=self.temperature,
           top_p=self.top_p,
           max_tokens=params.get("max_tokens", 256),
       )
      
       # Convert the response to the necessary structure
       choices = response.choices
       # Wrap the response in SimpleNamespace to make it compatible with AutoGen
       response_namespace = SimpleNamespace()
       response_namespace.choices = [
           SimpleNamespace(message=SimpleNamespace(content=choice.message.content))
           for choice in choices
       ]
       # Add a cost attribute (even if 0, since AutoGen expects it)
       response_namespace.cost = 0
      
       return response_namespace


   def message_retrieval(self, response):
       """Retrieve the assistant's response from the AI21 API response."""
       # Using attribute access for SimpleNamespace
       choices = response.choices
       return [choice.message.content for choice in choices]

   def cost(self, response) -> float:
       return response.cost


   @staticmethod
   def get_usage(response):
       return {
           "prompt_tokens": 0,
           "completion_tokens": 0,
           "total_tokens": 0,
           "cost": response.cost
       }



# Initialize Assistant and Register the AI21JambaModelClient
assistant = AssistantAgent("assistant", llm_config={"config_list": config_list_custom})
assistant.register_model_client(model_client_cls=AI21JambaModelClient)


# Set up the user proxy agent
user_proxy = UserProxyAgent(
   "user_proxy",
   code_execution_config={
       "work_dir": "coding",
       "use_docker": False
   }
)

"""
SCIENTISTS
"""
scientist_computer_vision_engineer = autogen.AssistantAgent(
    name="scientist_computer_vision_engineer",
    system_message = '''You are a sophisticated computer vision engineer trained in scientific research and innovation. You are collaborating with a group of scientists to discuss the technical content that will form the basis of a grant proposal. 
    
    Your primary task is to present your opinion on a certain subject, with the perspective of computer vision. Especially, present interesting recent discoveries in your field that could be further extended in this research grant. Also, explain how to combine these advances with that of the other fields in the discussion.

    Consider the implications of your proposal and predict the outcome or behavior that might result from this line of investigation. Your creativity in linking these concepts to address unsolved problems or propose new, unexplored areas of study, emergent or unexpected behaviors, will be highly valued.

    Be as quantitative as possible and include details such as numbers, sequences, or mathematical formulas. 

    You will have access to summaries of several recent research papers in the field of computer vision. Base your arguments based off the knowledge captured in those papers.

    """

    Summaries:
    summary: This paper presents a computer vision-based model for detecting road obstacles in construction zones, a crucial element for safe autonomous driving. The model, built on the YOLO framework, achieves impressive accuracy (over 94% mean average precision) and operates with a quick inference time of 1.6 milliseconds. This suggests that the system can effectively identify obstacles under varying conditions, improving road safety for autonomous vehicles. 


summary: This paper proposes a system for optimizing Tilapia feeding using computer vision and IoT technologies. It employs real-time sensors to monitor water quality and computer vision to analyze fish size, determining the optimal feed amount. YOLOv8 is used for keypoint detection to measure fish weight, achieving 94% precision on a dataset of 3,500 images. This method, incorporating data collection mirroring inference conditions, significantly improves feeding accuracy and could potentially increase production up to 58 times compared to traditional farms. 


summary: This paper proposes a novel fast architecture for real-time semantic segmentation named DuFNet. DuFNet proposes a novel Semantic Information Flow (SIF) structure for context information and a novel Fringe Information Flow (FIF) structure for spatial information. The SIF encodes the input stage by stage in the ResNet18 backbone and provides context information for the feature fusion module. The FIF consists of a pooling layer and an upsampling operator followed by projection convolution layer.  DuFNet achieved faster speed and comparable performance with 72.34% mIoU accuracy and 78 FPS on Cityscapes Dataset based on the ResNet18 backbone. 


summary: This research focuses on automating stem detection and classifying xylem wetness using a Scholander Pressure Chamber.  The goal is to improve SWP (stem water potential) measurement, which is crucial for efficient irrigation management in agriculture.  The study involved collecting video data and applying computer vision and machine learning techniques to identify stems and classify water emergence at the xylem.  The best performing model combination for this process was YOLOv8n for stem detection and ResNet50 for classification, achieving a Top-1 accuracy of 80.98%. 


summary: This study provides a detailed analysis of the YOLOv8 object detection model, examining its architecture, training methods, and performance improvements over prior versions like YOLOv5. Key advancements include the CSPNet backbone for enhanced feature extraction, the FPN+PAN neck for superior multi-scale object detection, and the shift to an anchor-free approach. The paper evaluates YOLOv8's performance on benchmarks such as Microsoft COCO and Roboflow 100, showcasing its high accuracy and real-time capabilities across diverse hardware platforms. The study also explores YOLOv8's developer-friendly enhancements, including its unified Python package and CLI, which simplify model training and deployment. This research establishes YOLOv8 as a leading solution in the evolving object detection domain. 


summary: This paper analyzes 30 years of computer vision research papers and patents, revealing a pipeline where computer vision research directly fuels surveillance technologies. The analysis of over 40,000 documents shows that a vast majority of these papers and patents explicitly state their technology is capable of extracting human data, particularly about the body and its parts. The paper highlights how leading universities and tech corporations play a key role in this pipeline, with their research being cited in thousands of surveillance patents. The study counters the narrative that only a few entities are responsible for surveillance, demonstrating how the entire field contributes to it. The number of papers with downstream surveillance patents has increased fivefold since the 1990s, with computer vision research now used in over 11,000 surveillance patents. The paper further reveals how language used in these documents obfuscates the extent of surveillance. 


summary: This paper presents a mobile imaging system for assessing road safety in urban areas. The system uses computer vision techniques to identify irregularities like missing street lights, damaged roads, and traffic violations.  The system was tested on 2000 km of unconstrained roads in an entire city, generating city-level safety maps. The authors investigated the performance of these techniques under various conditions, including different road types, lighting, and weather.  This system offers a cost-effective and scalable solution for road safety monitoring. 


summary: This paper introduces a reconfigurable CMOS image sensor (CIS) system that improves energy efficiency in computer vision applications. It achieves this by selectively skipping uneventful regions or rows during the sensor's readout and analog-to-digital conversion (ADC) phases. A novel masking algorithm directs this skipping process in real-time, optimizing both the front-end sensor and back-end neural networks for applications such as autonomous driving and augmented/virtual reality (AR/VR). The system can operate in standard mode without skipping, depending on application needs. Evaluations on object detection and gaze estimation datasets demonstrate up to 53% reduction in front-end sensor energy while maintaining state-of-the-art accuracy. 


summary: This paper describes the research experience of a computer engineering undergraduate student working with computer vision and robotics. The student explored the use of optical flow to detect moving objects, detailing the challenges faced and solutions used. The paper highlights the development of both technical skills and interpersonal skills related to teamwork and diversity. It also emphasizes the importance of learning process, problem-solving and creative thinking. 


summary: This paper proposes a vision-based system for automatic grocery tracking in smart homes. It addresses the challenge of tracking groceries in a home environment by combining retail shelving data and fruit datasets with real-time 360-degree views of home grocery storage. By integrating this object detection system with supply chain and user food interest prediction systems, the authors aim to achieve complete automation of grocery ordering. 


summary: This report focuses on the problem of quickly annotating video frames with bounding boxes for a novel object. The authors present a user interface and workflow specifically designed to make this process fast, even for unfamiliar objects. 


summary: Existing object detection methods rely on neural networks and deep learning for applications such as autonomous driving and aerial photography. These methods are vulnerable to factors such as illumination, occlusion, and viewing angle. This study uses convolutional neural networks (CNN) to recognize objects, leveraging their advantages of end-to-end learning, sparse relations, and weight sharing. The study focuses on classifying objects based on their detected bounding box position, exploring recognition accuracy under varying distances. Results show that accuracy is influenced by the object proportion and number of samples: smaller objects and fewer samples lead to higher accuracy. The study emphasizes the need for cost-effective object recognition systems, especially in the context of the global economic impact of the pandemic. The authors propose a custom dataset and utilize the Yolov2 model for training and testing, demonstrating the effectiveness of neural networks in improving object recognition rates. 


summary: This paper explores the effectiveness of simple visual sensors, like single photoreceptors, in solving computer vision tasks. The researchers demonstrate that even with resolutions as low as one-by-one pixel, these sensors can achieve performance comparable to high-resolution cameras in tasks like visual navigation and continuous control. They highlight the importance of sensor design and present a computational optimization algorithm to find well-performing designs. The paper also includes a human survey to evaluate the effectiveness of intuitive designs. 


summary: Object detection is a well-studied problem in autonomous driving, particularly for pedestrian detection. However, object detection using fisheye cameras for near-field sensing has been less explored. The standard bounding box representation struggles with fisheye cameras due to radial distortion. This paper investigates alternative representations for object detection, including rotated bounding boxes, ellipses, polygons, and polar arc/angle representations. The proposed FisheyeDetNet model, using polygons, outperforms other approaches, achieving a mAP score of 49.5% on the Valeo fisheye surround-view dataset. This dataset comprises 60,000 images captured from four surround-view cameras across different regions. This research is the first detailed study on object detection using fisheye cameras for autonomous driving. 


summary: This paper introduces an enhanced self-checkout system for retail stores that leverages an improved version of the YOLOv10 network. The system aims to boost checkout efficiency and reduce labor costs. It achieves this by implementing targeted optimizations to the YOLOv10 model, including the incorporation of the detection head structure from YOLOv8, which results in improved product recognition accuracy. Additionally, a specialized post-processing algorithm tailored for self-checkout scenarios is developed to further enhance the system's performance. The paper claims that experimental results indicate that the system surpasses existing methods in terms of product recognition accuracy and checkout speed. This research provides a novel technical solution for retail automation and offers insights into optimizing deep learning models for real-world applications. 


summary: Early-stage identification of fruit flowers in both opened and unopened conditions in an orchard environment is crucial for crop load management operations such as flower thinning and pollination using automated and robotic platforms. This paper proposes a vision system that detects early-stage flowers in an unstructured orchard environment using the YOLOv5 object detection algorithm. The centroid of individual flowers (both open and unopen) is identified and associated with flower clusters via K-means clustering. The system achieves an accuracy of up to 81.9% mAP in detecting opened and unopened flowers in commercial orchard images. 


summary: DroneVis is a new Python library for automating computer vision algorithms on Parrot drones. It offers a variety of features and tasks, including various computer vision models. The library is well-documented, easy to customize, and available on Github. 


summary: This paper describes two computer vision systems designed to automatically count crustacean larvae in industrial ponds. The first system uses an iPhone 11 camera and a specially designed bucket to capture images of larvae in controlled conditions. The second system uses a DSLR Nikon D510 camera to capture images of larvae in outdoor conditions. Both systems employ a YOLOv5 CNN model to count the larvae, overcoming the challenge of their small size. The paper also details the development of a growth function for Macrobrachium Rosenberg's larvae, using data from 11 growth stages over 19 days.  The results show promising accuracy in both systems, with the first achieving an 88.4% accuracy and the second reaching 86%. 


summary: This paper explores the potential of computer vision in security and surveillance, presenting a novel approach to track motion in videos.  By categorizing motion into Arcs, Lanes, Converging/Diverging, and Random/Block motions using Motion Information Images and Blockwise dominant motion data, the paper examines different optical flow techniques, CNN models, and machine learning models. The results can train anomaly-detection models, provide behavioral insights based on motion, and enhance scene comprehension. 


summary: This study presents a novel driver drowsiness detection system that combines deep learning techniques with the OpenCV framework. The system utilizes facial landmarks extracted from the driver's face as input to Convolutional Neural Networks trained to recognize drowsiness patterns. The integration of OpenCV enables real-time video processing, making the system suitable for practical implementation. Extensive experiments on a diverse dataset demonstrate high accuracy, sensitivity, and specificity in detecting drowsiness. The proposed system has the potential to enhance road safety by providing timely alerts to prevent accidents caused by driver fatigue. This research contributes to advancing real-time driver monitoring systems and has implications for automotive safety and intelligent transportation systems. The successful application of deep learning techniques in this context opens up new avenues for future research in driver monitoring and vehicle safety. The implementation code for the paper is available at this https URL. 


summary: This paper proposes a low-cost alternative to graphics tablets for online educators called "Do-It-Yourself Graphics Tab" or "DIY Graphics Tab".  It uses computer vision to capture images of a person writing on paper with a webcam and generates an output screen containing the written content.  This solution addresses the high cost of graphics tablets for many instructors and requires only a pen, paper, and a webcam. The paper outlines challenges faced by the system, such as hand occlusion, paper movement, and lighting conditions, and describes a pipeline that uses instance segmentation and preprocessing to overcome these obstacles. User experience evaluations from teachers and students are also discussed. 


summary: This paper investigates the YOLOv5 model for cattle identification in yards. The current solution using RFID tags has limitations with lost or damaged tags. This research utilizes YOLOv5 with eight different backbones and investigates the impact of mosaic augmentation on the model's performance. The results show that YOLOv5 with a transformer backbone achieved the highest accuracy, with a mean Average Precision (mAP) of 0.995. Mosaic augmentation significantly improved the model's accuracy across all backbones. The study concludes that YOLOv5 holds excellent potential for automatic cattle identification. 


summary: This paper proposes a novel reCAPTCHA system called arXiv reCAPTCHA, designed to be more robust to adversarial attacks. The system leverages the unique characteristics of the arXiv preprint repository, such as the abundance of scientific text and the high quality of submissions, to create a more challenging and less exploitable CAPTCHA. It utilizes a combination of natural language processing and computer vision techniques to analyze text and image content, ensuring that only genuine users can pass the challenge. The paper details the system's architecture, training process, and evaluation results, showcasing its improved security and user experience compared to traditional CAPTCHA approaches. 


summary: For distant iris recognition, a long focal length lens is generally used to ensure the resolution of iris images, which reduces the depth of field and leads to potential defocus blur. To accommodate users at different distances, it is necessary to control focus quickly and accurately. While for users in motion, it is expected to maintain the correct focus on the iris area continuously. In this paper, we introduced a novel rapid autofocus camera for active refocusing of the iris area of the moving objects using a focus-tunable lens. Our end-to-end computational algorithm can predict the best focus position from one single blurred image and generate a lens diopter control signal automatically. This scene-based active manipulation method enables real-time focus tracking of the iris area of a moving object. We built a testing bench to collect real-world focal stacks for evaluation of the autofocus methods. Our camera has reached an autofocus speed of over 50 fps. The results demonstrate the advantages of our proposed camera for biometric perception in static and dynamic scenes. The code is available at https://github.com/Debatrix/AquulaCam. 


summary: It is common practice to think of a video as a sequence of images (frames), and re-use deep neural network models that are trained only on images for similar analytics tasks on videos. This paper shows that this "leap of faith" that deep learning models that work well on images will also work well on videos is actually flawed. Even when a video camera is viewing a scene that is not changing in any human-perceptible way, the accuracy of video analytics application fluctuates noticeably. These fluctuations occur because successive frames produced by the video camera may look similar visually, but are perceived quite differently by the video analytics applications. The root cause for these fluctuations is the dynamic camera parameter changes that a video camera automatically makes in order to capture and produce a visually pleasing video. The camera inadvertently acts as an "unintentional adversary" because these slight changes in the image pixel values in consecutive frames have a noticeably adverse impact on the accuracy of insights from video analytics tasks that re-use image-trained deep learning models. To address this inadvertent adversarial effect from the camera, the authors explore the use of transfer learning techniques to improve learning in video analytics tasks through the transfer of knowledge from learning on image analytics tasks. Experiments with a number of different cameras, and a variety of different video analytics tasks, show that the inadvertent adversarial effect from the camera can be noticeably offset by quickly re-training the deep learning models using transfer learning.  


summary: This paper presents a real-time helmet violation detection system that uses a unique data processing strategy called "few-shot data sampling" and the YOLOv8 object detection model. The system was designed to operate in real-time and achieve high accuracy even with limited training data. The proposed method achieved a mean Average Precision (mAP) score of 0.5861 on experimental validation data, demonstrating its effectiveness and robustness. The code for the few-shot data sampling technique is available on GitHub. 


summary: Convolutional Neural Networks (CNNs) are often used for computer vision tasks, but they are compute-intensive and difficult to deploy on low-power devices. This paper proposes a method to improve efficiency by identifying and excluding irrelevant pixels from the input image. The authors found that 48% of pixels in three popular computer vision datasets (COCO, MOT Challenge, and PASCAL VOC) are irrelevant to the task. They developed a "focused convolution" to modify the CNN's convolutional layers to exclude these irrelevant pixels, resulting in a 45% reduction in inference latency, energy consumption, and multiply-add count on an embedded device without loss of accuracy. 


summary: This paper proposes a computer vision-based solution for automated crop field surveillance to address the problem of wild animal trespassing. The system aims to reduce crop loss and automate field security. The paper discusses the existing challenges faced by farmers due to wildlife damage, including high costs associated with traditional solutions like fences and the inefficacy of scare tactics. 


summary: Retail checkout systems typically rely on barcode scanners or QR codes, which are time-consuming, require human supervision, and result in long queues. This paper proposes ARC, a vision-based system that aims to make checkout faster, autonomous, and more convenient. ARC utilizes a convolutional neural network to identify objects placed beneath a webcam. The system was evaluated on a dataset of 100 local retail items and achieved reasonable accuracy. The project code and dataset are publicly available. 


summary: This study compares five YOLOv5 variants (YOLOv5n6s, YOLOv5s6s, YOLOv5m6s, YOLOv5l6s, and YOLOv5x6s) for vehicle detection in different environments. The research evaluates their performance in detecting various vehicle types (Car, Bus, Truck, Bicycle, and Motorcycle) under varying conditions (lighting, occlusion, and weather). Performance metrics like precision, recall, F1-score, and mean Average Precision are used to assess each model's accuracy and reliability. YOLOv5n6s shows a good balance between precision and recall, especially for detecting Cars. YOLOv5s6s and YOLOv5m6s improve recall, detecting more objects. YOLOv5l6s, with its larger capacity, performs well for Cars but struggles with Motorcycles and Bicycles. YOLOv5x6s is effective with Buses and Cars but has difficulties with Motorcycles. 


summary: Facial analysis is a popular area of research in computer vision. This paper presents a system-level design for a real-time facial analysis system. The system utilizes a collection of deep neural networks to perform various tasks including age, gender, and facial expression recognition, as well as facial similarity analysis. The paper investigates the parallelization and interaction between individual tasks to achieve high accuracy and real-time performance. The system's accuracy is comparable to state-of-the-art methods, and its recognition speed meets real-time requirements. Additionally, a multitask network is proposed for joint prediction of age, gender, and facial expression. The source code and trained models are available online. 


summary: ## Abstract:

Given the growing urban population and the resulting traffic congestion, the development of smart parking systems has become increasingly important. Smart parking solutions use cameras, sensors, and algorithms like computer vision to identify available parking spaces. This approach improves parking spot recognition, reduces traffic and pollution, and optimizes travel time. Recent years have seen a rise in the use of computer vision-based methods. However, many existing studies rely on manually labeled parking spots, which poses challenges in terms of cost and practical implementation. 

To address this, we propose a novel approach called PakLoc, which automatically localizes parking spots. Additionally, we introduce the PakSke module, which automatically adjusts the rotation and size of detected bounding boxes. Our methodology, evaluated on the PKLot dataset, results in a significant reduction in human labor by 94.25%. 

Another crucial aspect of a smart parking system is its ability to accurately determine and indicate the state of parking spots within a parking lot. The traditional approach involves using classification techniques to predict the status of parking spots based on bounding boxes derived from manually labeled grids. In this study, we present a novel approach called PakSta for automatically identifying the state of parking spots. Our method utilizes object detection from PakLoc to simultaneously determine the occupancy status of all parking spots within a video frame. PakSta demonstrates competitive performance on the PKLot dataset compared to other classification methods. 


summary: This paper examines the occlusion problem in cattle detection using unmanned aerial vehicles (UAVs).  The authors compare three cutting-edge object detection algorithms - YOLOv7, RetinaNet with ResNet50 backbone, RetinaNet with EfficientNet, and Mask RCNN - to identify hidden cattle in drone-captured datasets.  Experimental results demonstrate that YOLOv7 outperforms the other algorithms, achieving a precision of 0.612. The study focuses on improving cattle detection accuracy, particularly in challenging scenarios where animals are partially obscured. 


summary: With advancements in technology, computers now have the processing power to handle real-time images. Face recognition is commonly used for security and commercial applications, and AI has boosted its usage across many fields, including education. This study utilizes deep learning for object detection in images, specifically to track student attendance at an educational institution. The system captures images from a camera and analyzes them with image processing algorithms to record student attendance. This application is currently being tested at a school for the 2022-2023 academic year. 


summary: This research explores the application of deep learning in autonomous driving computer vision technology. Using advanced technologies such as convolutional neural networks (CNN), multi-task joint learning methods, and deep reinforcement learning, the article analyzes the application of deep learning in image recognition, real-time target tracking and classification, environment perception and decision support, and path planning and navigation. The proposed system achieves over 98% accuracy in image recognition, target tracking, and classification, and demonstrates efficient performance in environmental perception and decision support, path planning, and navigation. The conclusion highlights that deep learning significantly improves the accuracy and real-time response capabilities of autonomous driving systems. While challenges in environmental perception and decision support remain, the advancement of technology is expected to lead to wider applications and greater potential in the future. 


summary: This project explores how machine learning and computer vision can be used to improve accessibility for people with visual impairments. The paper proposes a mobile application that uses audio and haptic feedback to help blind people orient themselves in space.  The application will have three main features: 1) scanning text from a camera and reading it to the user, 2) detecting objects and providing audio feedback about their location, and 3) currency detection, which provides the user with the total amount of currency value through the camera. 


summary: The paper "YOLO OBJECT DETECTION USING OPENCV" focuses on the challenges of object detection in computer vision. The goal is to create algorithms that can recognize objects and their location within images. While object detection is a complex task, the paper aims to address these challenges by utilizing the YOLO (You Only Look Once) object detection model with OpenCV.  The authors propose an approach that leverages a trained YOLO model to perform object detection and presents a detailed breakdown of the technical implementation.  This paper aims to overcome limitations of existing systems and improve the accuracy, up-to-dateness, and efficiency of object detection. 


summary: This research paper focuses on the detection and tracking of pedestrians from video sequences. It explores how computer vision and pattern recognition can be combined to achieve this, emphasizing the importance of this technology in various applications like target recognition and behavior understanding.  The paper proposes a binary function based on importance and uses space representation to minimize noise impact on the tracking algorithm. The color band learning method is then implemented to update the target template online and account for changes in pedestrian appearance. Experimental results demonstrate the system's effectiveness in tracking even with significant changes in appearance and posture. 


summary: This paper proposes a novel method for intelligent streetlight management using a smart CCTV camera and semantic segmentation. The system automatically adjusts streetlight brightness based on the presence of pedestrians or vehicles detected in the CCTV footage, dimming the lights when no activity is present. This approach also differentiates between day and night, enabling automated ON/OFF switching for energy conservation. The model is trained using a U-net architecture with ResNet-34 as its backbone, and its effectiveness is validated through assessment metrics. This solution is presented as a cost-effective, energy-efficient, and resilient alternative to conventional streetlight management systems. 


summary: Image classification models, including convolutional neural networks (CNNs), perform well on a variety of classification tasks but struggle under conditions of partial occlusion, i.e., conditions in which objects are partially covered from the view of a camera. Methods to improve performance under occlusion, including data augmentation, part-based clustering, and more inherently robust architectures, including Vision Transformer (ViT) models, have, to some extent, been evaluated on their ability to classify objects under partial occlusion. However, evaluations of these methods have largely relied on images containing artificial occlusion, which are typically computer-generated and therefore inexpensive to label. Additionally, methods are rarely compared against each other, and many methods are compared against early, now outdated, deep learning models. We contribute the Image Recognition Under Occlusion (IRUO) dataset, based on the recently developed Occluded Video Instance Segmentation (OVIS) dataset (arXiv:2102.01558). IRUO utilizes real-world and artificially occluded images to test and benchmark leading methods' robustness to partial occlusion in visual recognition tasks. In addition, we contribute the design and results of a human study using images from IRUO that evaluates human classification performance at multiple levels and types of occlusion. We find that modern CNN-based models show improved recognition accuracy on occluded images compared to earlier CNN-based models, and ViT-based models are more accurate than CNN-based models on occluded images, performing only modestly worse than human accuracy. We

summary: The DifuzCam design replaces a traditional camera lens with a mask and uses a pre-trained diffusion model for image reconstruction. This approach allows for a significantly smaller and lighter camera while maintaining high image quality. The model can leverage textual descriptions of the captured scene to further improve image reconstruction. 


summary: This paper proposes a method for analyzing classroom teaching behavior using intelligent image recognition. It utilizes a fast target detection method based on FFmpeg CODEC, extracts MHI-HOG joint features from the detected foreground target area, and employs a BP neural network support vector machine joint classifier to recognize behavior. The method achieves high accuracy in motion detection (95%) and foreground detection (90% time savings), while the MHI-HOG joint feature-based behavior classification and recognition system has a comprehensive recognition rate of 95%. The built-in BP neural network support vector machine demonstrates 97% accuracy in extracting, classifying, and recognizing single sample characteristics. The study aims to identify and analyze classroom behavior and validate the effectiveness of the proposed collaborative classifiers for building an intelligent classroom. 


summary: This paper focuses on designing a Raspberry Pi system with a camera that can detect and count objects within a target area. The system utilizes Python programming due to its compatibility with Raspberry Pi and its ease of use for rapid application development. The results show that the system successfully detects and counts different objects in an image, achieving an average efficiency of 90.206%, demonstrating high reliability. 


summary: Open-vocabulary detection (OVD) aims to detect objects beyond a predefined set of categories. YOLO-World, a pioneering model incorporating the YOLO series into OVD, prioritizes speed and efficiency. However, its performance is limited by its neck feature fusion mechanism. Mamba-YOLO-World, a novel YOLO-based OVD model, addresses these limitations by using the proposed MambaFusion Path Aggregation Network (MambaFusion-PAN) as its neck architecture. This new architecture utilizes a State Space Model-based feature fusion mechanism with linear complexity and globally guided receptive fields, outperforming YOLO-World on COCO and LVIS benchmarks while maintaining comparable parameters and FLOPs. Mamba-YOLO-World also surpasses existing state-of-the-art OVD methods with fewer parameters and FLOPs. 


summary: Precision agriculture aims to use technological tools for the agro-food sector to increase productivity, cut labor costs, and reduce the use of resources. This work takes inspiration from bees' vision to design a remote sensing system tailored to incorporate UV-reflectance into a flower detector. We demonstrate how this approach can provide feature-rich images for deep learning strawberry flower detection and we apply it to a scalable, yet cost effective aerial monitoring robotic system in the field. We also compare the performance of our UV-G-B image detector with a similar work that utilizes RGB images. 


summary: Real-time object detection in indoor settings is challenging due to variable lighting and complex backgrounds. This paper addresses this by evaluating existing datasets and models, creating a refined dataset focused on 32 relevant indoor categories derived from OpenImages v7. It then presents an adaptation of a CNN detection model with an attention mechanism to improve feature identification in cluttered scenes. The study demonstrates that this approach outperforms existing models in both accuracy and speed, opening new avenues for research and applications in real-time indoor object detection. 


summary: This paper introduces FA-YOLO, a novel object detection model that improves upon YOLOv9 by incorporating two new modules: the Fine-grained Multi-scale Dynamic Selection Module (FMDS) and the Adaptive Gated Multi-branch Focus Fusion Module (AGMF).  The FMDS module enhances detection accuracy for various object sizes by dynamically selecting and fusing multi-scale features. The AGMF module further refines feature fusion through parallel branches, incorporating information from gated units, the FMDS module, and TripletAttention. Experimental results on the PASCAL VOC 2007 dataset show FA-YOLO achieves a 1.0% improvement in mean Average Precision (mAP) compared to YOLOv9, reaching 66.1%. This improvement is particularly notable for small, medium, and large targets, with FA-YOLO demonstrating gains of 2.0%, 3.1%, and 0.9% respectively. 


summary: This paper proposes a novel design and implementation method for real-time multi-area target individual detection on video, where the detection areas are defined by freehand drawing on the video display. The drawn areas are represented as polylines with color changes indicating the drawing or detection stage. The shape of the drawn areas is customizable, and they operate independently. The detection results are presented via a Tkinter-based GUI. While the object recognition model is currently based on YOLOv5, the core design is model-independent. Using PIL, OpenCV, and Tkinter, the drawing and detection processes are real-time and efficient. The proposed design is basic and can be extended for various monitoring and detection applications. 


summary: Current parking area perception algorithms rely on limited range detection and error-prone homographic projection, but Advanced Driver Assistance Systems (ADAS) need comprehensive and intelligent Human-Machine Interfaces (HMIs) for user interaction. This paper introduces Multi-Task Fisheye Cross View Transformers (MT F-CVT) that uses a four-camera fisheye Surround-view Camera System (SVCS) to create a detailed Bird-Eye View (BEV) grid feature map. This map is processed by both a segmentation decoder and a Polygon-Yolo based object detection decoder for parking slots and vehicles. Trained on LiDAR labeled data, MT F-CVT accurately positions objects in real open-road scenes, achieving an F-1 score of 0.89. The smaller model operates at 16 fps on an Nvidia Jetson Orin board with similar detection results, demonstrating robust generalization. A demo video is available at the provided link. 


summary: Automating fruit and vegetable detection using computer vision is crucial for modernizing agriculture and improving efficiency. This paper presents an end-to-end pipeline for detecting and localizing fruits and vegetables in real-world scenarios. To achieve this, they curated a dataset named FRUVEG67 with images of 67 fruit and vegetable classes captured in unconstrained scenarios. They also developed a semi-supervised data annotation algorithm (SSDA) to generate bounding boxes for objects in the non-annotated images. For detection, they introduced the Fruit and Vegetable Detection Network (FVDNet), an ensemble version of YOLOv7 featuring three distinct grid configurations. Their experimental results highlight the superiority of FVDNet compared to previous versions of YOLO, showcasing remarkable improvements in detection and localization performance. They achieved an impressive mean average precision (mAP) score of 0.78 across all classes. 


summary: In static monitoring cameras, useful contextual information can stretch far beyond the few seconds typical video understanding models might see: subjects may exhibit similar behavior over multiple days, and background objects remain static. Due to power and storage constraints, sampling frequencies are low, often no faster than one frame per second, and sometimes are irregular due to the use of a motion trigger. In order to perform well in this setting, models must be robust to irregular sampling rates. In this paper we propose a method that leverages temporal context from the unlabeled frames of a novel camera to improve performance at that camera. Specifically, we propose an attention-based approach that allows our model, Context R-CNN, to index into a long term memory bank constructed on a per-camera basis and aggregate contextual features from other frames to boost object detection performance on the current frame. We apply Context R-CNN to two settings: (1) species detection using camera traps, and (2) vehicle detection in traffic cameras, showing in both settings that Context R-CNN leads to performance gains over strong baselines. Moreover, we show that increasing the contextual time horizon leads to improved results. When applied to camera trap data from the Snapshot Serengeti dataset, Context R-CNN with context from up to a month of images outperforms a single-frame baseline by 17.9% mAP, and outperforms S3D (a 3d convolution based baseline) by 11.2% mAP. 


summary: This paper proposes a novel video-based, two-stream deep neural network approach for automatic pain state recognition in dogs. The approach extracts and preprocesses body keypoints, and computes features from both keypoints and the RGB representation over the video. It also addresses self-occlusions and missing keypoints. The paper introduces a unique video-based dog behavior dataset, collected and annotated by veterinary professionals, and reports good classification results with the proposed approach. This study is one of the first works on machine learning based estimation of dog pain state. 


summary: This paper proposes a computer vision-based framework for detecting road traffic crashes (RTCs) using surveillance cameras. The system, comprised of five modules, utilizes YOLO for vehicle detection, MOSSE tracker for vehicle tracking, and a novel collision estimation method for accident detection. Violence flow descriptor (ViF) and SVM classifier are employed for crash prediction. Finally, a GPS and GSM module sends a notification to emergency services with the location, time, and date of the accident. The goal is to achieve high accuracy with minimal false alarms using a pipelined approach. 


summary: This study evaluated the performance of YOLOv8 model configurations for instance segmentation of strawberries into ripe and unripe stages in an open field environment. The YOLOv8n model demonstrated superior segmentation accuracy with a mean Average Precision (mAP) of 80.9%, outperforming other YOLOv8 configurations. It processed images at 12.9 milliseconds, while the least-performing model, YOLOv8s, processed at 22.2 milliseconds. Overall, YOLOv8n achieved the fastest inference speed of 24.2 milliseconds, outperforming YOLOv8s, YOLOv8m, YOLOv8l, and YOLOv8x. These results highlight the potential of advanced object segmentation algorithms to address complex visual recognition tasks in open-field agriculture effectively. 


summary: Object detection is essential for traffic management, autonomous vehicles, and smart cities. However, detecting small objects in images captured by distant cameras is challenging due to their size, distance, and cluttered backgrounds. To overcome these challenges, this paper introduces SOD-YOLOv8, a model specifically designed for small object detection in traffic scenes. SOD-YOLOv8 improves multi-path fusion within YOLOv8 to integrate features across different levels, enhances feature extraction with an Efficient Multi-Scale Attention Module, and introduces a new loss function called Powerful-IoU. The result is a model that significantly outperforms existing methods in small object detection, achieving higher recall, precision, and mAP without compromising computational efficiency. 


summary: This paper explores the application of computer vision in intelligent computing. It utilizes face recognition as a case study, applying image recognition, feature point extraction using the K-means clustering algorithm, and histogram-based classification modeling. The study focuses on extracting data for vision recognition, even in the presence of obstacles. Results highlight computer vision's potential as a key development area in artificial intelligence, enabling machines to perceive, recognize, track, and measure objects in a manner analogous to human vision. 


summary: This paper proposes a new methodology for estimating the geolocation of target vehicles in a GPS coordinate system using a monocular camera mounted on a moving vehicle. The methodology combines deep learning, image processing, and geometric computation to address the observed-vehicle localization problem. Real-world traffic data was used to evaluate the proposed algorithms, which effectively estimated the observed vehicle's latitude and longitude dynamically. 


summary: The MINSU (Mobile Inventory and Scanning Unit) algorithm uses computer vision to estimate the amount of material in a cabinet. The process involves five steps: object detection, foreground subtraction, K-means clustering, percentage estimation, and counting. Object detection identifies the cabinet's position, while foreground subtraction isolates the cabinet from the background. K-means clustering simplifies the image for analysis, and percentage estimation determines the proportion of the cabinet filled with material. Finally, the algorithm uses the percentage to estimate the quantity of materials inside the cabinet. 


summary: This paper proposes a new method for generating region proposals in object detection by using an event camera. The authors draw an analogy between the human eye's rod cells and the event camera, both of which detect changes in light intensity. They argue that the event camera can act as a region proposal network (RPN) in deep learning, similar to how the rods act as an RPN in human vision. By replacing the traditional RPN in Mask R-CNN with an event camera, the authors achieve faster object detection with comparable accuracy, making it suitable for fast applications. 


summary: This paper investigates real-time pedestrian recognition on small physical-size computers with low computational resources for faster speed. Three methods are presented: improved Local Binary Pattern (LBP) features and Adaboost classifier, optimized Histogram of Oriented Gradients (HOG) and Support Vector Machine, and fast Convolutional Neural Networks (CNNs). Results show that these methods achieve real-time pedestrian recognition with over 95% accuracy and over 5 fps on a small platform with a 1.8 GHz Intel i5 CPU. These methods are easily adaptable to small mobile devices, offering high compatibility and generality. 


summary: By analyzing the motion of people and other objects in a scene, we demonstrate how to infer depth, occlusion, lighting, and shadow information from video taken from a single camera viewpoint. This information is then used to composite new objects into the same scene with a high degree of automation and realism. In particular, when a user places a new object (2D cut-out) in the image, it is automatically rescaled, relit, occluded properly, and casts realistic shadows in the correct direction relative to the sun, and which conform properly to scene geometry. We demonstrate results (best viewed in supplementary video) on a range of scenes and compare to alternative methods for depth estimation and shadow compositing. 


summary: Accurate crop row detection is often challenged by varying field conditions. Traditional color-based segmentation struggles with these variations, and a lack of comprehensive datasets hinders the development of robust models. This paper presents a dataset for crop row detection with 11 field variations from Sugar Beet and Maize crops. A novel crop row detection algorithm is introduced that can detect crop rows under varying conditions, including curved rows, weeds, discontinuities, growth stages, tramlines, shadows, and light levels. The algorithm uses only RGB images from a front-mounted camera on a Husky robot and outperforms traditional color-based methods. Dense weed presence and discontinuities in crop rows were the most challenging conditions. The method can detect the end of a crop row and navigate the robot towards the headland area. 


summary: The paper explores the use of computer vision techniques to automate bee counting, which can help monitor bee colony health, analyze blooming periods, and investigate the effects of agricultural spraying. The authors compare three methods and find that a ResNet-50 convolutional neural network classifier achieves the best performance, reaching 87% accuracy on the BUT1 dataset and 93% accuracy on the BUT2 dataset. 


summary: Online exams via video conference software like Zoom have been adopted in many schools due to COVID-19. While it is convenient, it is challenging for teachers to supervise online exams from simultaneously displayed student Zoom windows. In this paper, we propose iExam, an intelligent online exam monitoring and analysis system that can not only use face detection to assist invigilators in real-time student identification, but also be able to detect common abnormal behaviors (including face disappearing, rotating faces, and replacing with a different person during the exams) via a face recognition-based post-exam video analysis. To build such a novel system in its first kind, we overcome three challenges. First, we discover a lightweight approach to capturing exam video streams and analyzing them in real time. Second, we utilize the left-corner names that are displayed on each student's Zoom window and propose an improved OCR (optical character recognition) technique to automatically gather the ground truth for the student faces with dynamic positions. Third, we perform several experimental comparisons and optimizations to efficiently shorten the training and testing time required on teachers' PC. Our evaluation shows that iExam achieves high accuracy, 90.4% for real-time face detection and 98.4% for postexam face recognition, while maintaining acceptable runtime performance. We have made iExam's source code available at https://github.com/VPRLab/iExam. 


summary: Current computer vision (CV) systems use an image signal processing (ISP) unit to convert raw images to RGB images.  However, this process can be computationally expensive, especially for low-power devices.  Recent works have proposed in-sensor and in-pixel computing approaches to bypass the ISP, but this can lead to accuracy degradation due to the difference in covariance between raw and processed images.  To address this issue, we propose to invert the ISP pipeline to enable training on raw images, which leads to a 7.1% increase in test accuracy.  We also propose an energy-efficient form of analog in-pixel demosaicing to further improve accuracy and reduce energy consumption, resulting in an 8.1% increase in mAP.  Finally, we demonstrate a 20.5% increase in mAP using few-shot learning on raw images from the PASCALRAW dataset. 


summary: This work studies the dynamic between research in the computer vision industry and academia. The results are demonstrated on a set of top-5 vision conferences. The study quantifies the share of industry-sponsored research, showing an increasing proportion of papers published by industry-affiliated researchers and more academics joining or collaborating with companies. It explores the impact of industry presence on research topics and citation patterns, finding similar topic distributions but a strong preference towards citing industry papers. Finally, it investigates possible reasons for citation bias, such as code availability and influence. 


summary: Visual recognition is crucial for harvesting robots, but unstructured environments pose challenges to detection accuracy. This paper proposes an improved YOLO v4 model, called YOLO v4+, to address these challenges.  YOLO v4+ incorporates an attention mechanism for feature refinement, a multi-scale feature fusion module, and a modified focal loss function. Experiments show that YOLO v4+ achieves an average precision of 94.25% and an F1 score of 93%, outperforming the original YOLO v4.  The model demonstrates high comprehensive and generalization abilities and can be applied to harvesting robots for enhanced robustness. 


summary: This paper proposes an object detection model for smart surveillance systems (3s) utilizing the YOLO v3 deep learning architecture. The model utilizes a transfer learning approach and the MS COCO dataset for training, achieving a high accuracy of 99.71% and an improved mean Average Precision (mAP) of 61.5.  This approach aims to address the need for efficient object detection in real-time surveillance systems, contributing to the advancement of global security measures. 


summary: This paper proposes a new obstacle detection and recognition model based on a computer-expanded convolutional neural network (CNN).  The model uses dilated convolutions to learn features from the original image without needing preprocessing, and it can achieve accurate recognition of obstacle types. The proposed model is highly accurate, has good generalization capability, and can be used in real-time applications. The model was built by combining a hierarchical expanded CNN structure with a Region of Interest (ROI) algorithm. The model was able to learn the features of various obstacle types and extract global features with characterization significance.  This enables real-time obstacle detection and high-accuracy type recognition. 


summary: Teaching Computer Science (CS) by having students write programs by hand on paper offers several advantages, including focused learning, careful thinking, and reduced cognitive load for beginners. However, the lack of tools for working with handwritten programs poses a challenge. The paper presents two innovative methods for handwritten code recognition:

1. **Combined OCR, indentation recognition, and a language model for post-OCR error correction:** This method surpasses existing systems, reducing error from 30% to 5% with minimal hallucinations.

2. **Multimodal language model for end-to-end recognition:** This method directly recognizes handwritten programs without relying on OCR.

The authors believe their contributions can stimulate further research in CS education and promote accessibility. A dataset of handwritten programs and code is released to support future work. 


summary: This paper introduces CCTVCV, a computer vision model capable of accurately detecting CCTV cameras in images and video frames. The model was trained using 8387 manually annotated images containing 10419 CCTV camera instances, achieving an accuracy of up to 98.7%. The paper outlines the challenges associated with this research, presents a comprehensive comparison of model performance, and discusses potential privacy, safety, and security applications. The authors release the data and code as open-source for further validation and expansion. 


summary: Activity recognition computer vision algorithms can be used to detect the presence of autism-related behaviors, including what are termed "restricted and repetitive behaviors", or stimming, by diagnostic instruments. The limited data that exist in this domain are usually recorded with a handheld camera which can be shaky or even moving, posing a challenge for traditional feature representation approaches for activity detection which mistakenly capture the camera's motion as a feature. To address these issues, we first document the advantages and limitations of current feature representation techniques for activity recognition when applied to head banging detection. We then propose a feature representation consisting exclusively of head pose keypoints. We create a computer vision classifier for detecting head banging in home videos using a time-distributed convolutional neural network (CNN) in which a single CNN extracts features from each frame in the input sequence, and these extracted features are fed as input to a long short-term memory (LSTM) network. On the binary task of predicting head banging and no head banging within videos from the Self Stimulatory Behaviour Dataset (SSBD), we reach a mean F1-score of 90.77% using 3-fold cross validation (with individual fold F1-scores of 83.3%, 89.0%, and 100.0%) when ensuring that no child who appeared in the train set was in the test set for all folds. This work documents a successful technique for training a computer vision classifier which can detect human motion with few training examples

summary: This paper benchmarks various deep learning techniques for violence recognition from video data. The study uses a complex dataset and then tests the impact of increasing the dataset size from 500 to 1,600 videos. The results show an average accuracy improvement of 6% across four models. 


summary: Hermit crabs are important for coastal ecosystems, acting as indicators of marine health. Traditional survey methods are inefficient, so this study proposes a new approach using drones and deep learning to monitor them.  Super-Resolution Reconstruction (SRR) improves image quality, while a modified YOLOv8s network (CRAB-YOLO) increases detection accuracy. The system achieved a mean average precision (mAP) of 69.5%, showing promise for cost-effective and automated hermit crab monitoring. 


summary: This paper proposes a YOLOv8-based framework for layout hotspot detection, aiming to improve the efficiency of design rule checking (DRC). The method utilizes PCA to extract auxiliary information from the layout image and incorporates this information as an additional color channel, improving the accuracy of multi-hotspot detection while reducing false alarms.  Evaluations on ICCAD-2019 benchmark datasets show a precision of 83% and recall of 86%, with a false alarm rate below 7.4%. The augmentation approach also improved detection of "never-seen-before" hotspots by approximately 10%. 


summary: Shortage of labor in fruit crop production has become a significant challenge. To address this, automated machines are being developed to perform tasks like harvesting, pruning, and thinning. This study proposes a machine vision system to estimate crop load in apple orchards using an RGB-D sensor and a YOLOv8-based instance segmentation technique. This system identifies trunks and branches, estimates branch diameter and orientation using Principal Component Analysis, and calculates the limb cross-sectional area (LCSA) which is used for crop-load estimation. The system achieved an RMSE of 2.08 mm for branch diameter estimation and 3.95 for crop-load estimation, demonstrating the potential for automated decision-making in fruit yield management. 


summary: The lack of tamper-proof cattle identification technology in Bangladesh was a significant barrier for livestock insurance, leading to financial hardship for farmers. This paper presents a novel muzzle-based cattle identification system using AI to address this issue. The system utilizes the uniqueness of cattle muzzles, which are akin to human fingerprints. The researchers collected 32,374 images of 826 cattle and employed image processing techniques, including CLAHE and sharpening filters, to enhance the image quality. YOLO algorithm was used for cattle muzzle detection, and FaceNet architecture was used for feature extraction, resulting in a system with an accuracy of 96.489%, F1 score of 97.334%, and a remarkably low false positive rate of 0.098%. This system promises to significantly advance livestock insurance and precision farming. 


summary: Roads in medium-sized Indian towns often have lots of traffic but no (or disregarded) traffic stops, making it difficult for the blind to cross safely. This paper introduces INDRA, a dataset of 104 videos (26,000 frames) recorded from a pedestrian's perspective on Indian roads, annotated with road crossing safety labels and vehicle bounding boxes.  The authors train various classifiers on this data, including convolutional neural networks (CNNs), and develop a novel single-image architecture, DilatedRoadCrossNet, for deployment on the Nvidia Jetson Nano.  This model achieves 79% recall at 90% precision on unseen images. The paper concludes with a description of a wearable road crossing assistant running DilatedRoadCrossNet that can help the blind cross Indian roads in real-time. 


summary: This paper presents a fall detection system using the YOLOv5mu model, achieving a mean average precision (mAP) of 0.995. The system utilizes advanced data augmentation techniques for robustness and adaptability, offering precise, real-time fall detection within smart homes. The authors plan to further enhance the system by incorporating contextual data and exploring multi-sensor approaches for improved performance in diverse environments. 


summary: This research presents a resource-efficient framework for anomaly recognition in surveillance videos. The proposed Temporal based Anomaly Recognizer (TAR) combines a partial shift strategy with a 2D convolutional architecture-based model (MobileNetV2). Experiments on the UCF Crime dataset show an accuracy of 88%, exceeding current state-of-the-art performance. The TAR framework also achieves 52.7% accuracy for multiclass anomaly recognition on the UCF Crime2Local dataset.  The model can handle six camera streams simultaneously in real-time settings without requiring additional resources. 


summary: This paper presents a deep learning framework for real-time vehicle and pedestrian detection. The authors trained and evaluated different versions of YOLOv8 and RT-DETR models on a dataset representing complex urban settings.  YOLOv8 Large emerged as the most effective model, particularly for pedestrian recognition, achieving high precision and robustness. The results, including Mean Average Precision and recall rates, demonstrate the model's potential to significantly improve traffic monitoring and safety. 


summary: Accurately detecting student behavior in classroom videos can aid in analyzing their classroom performance and improving teaching effectiveness. However, the current accuracy rate in behavior detection is low. To address this challenge, we propose the Student Classroom Behavior Detection method, based on improved YOLOv7. First, we created the Student Classroom Behavior dataset (SCB-Dataset), which includes 18.4k labels and 4.2k images, covering three behaviors: hand raising, reading, and writing. To improve detection accuracy in crowded scenes, we integrated the biformer attention module and Wise-IoU into the YOLOv7 network. Finally, experiments were conducted on the SCB-Dataset, and the model achieved an mAP@0.5 of 79%, resulting in a 1.8% improvement over previous results. The SCB-Dataset and code are available for download at: https://github.com/Whiffe/SCB-dataset. 


summary: This paper presents a visual geo-localization system that determines the geographic locations of places (buildings and road intersections) from images without relying on GPS data. The approach combines Scale-Invariant Feature Transform (SIFT) for place recognition, traditional image processing for identifying road junction types, and deep learning using the VGG16 model for classifying road junctions. The most effective techniques have been integrated into an offline mobile application, improving accessibility for users in GPS-denied environments. 


summary: This study evaluated the performance of different configurations of YOLOv8, YOLOv9, and YOLOv10 object detection algorithms for fruitlet detection in commercial orchards. The research compared 17 configurations across the three YOLO versions, with YOLOv9 achieving the highest mAP@50 (0.935) and YOLOv10x demonstrating superior precision and recall. While YOLOv10x had the highest precision (0.908), YOLOv10s had the highest recall (0.872) within the YOLOv10 family. Additionally, YOLOv10b, YOLOv10l, and YOLOv10x exhibited faster post-processing speeds compared to other configurations. 


summary: Autofocus is an important task for digital cameras, yet current approaches often exhibit poor performance. We propose a learning-based approach to this problem, and provide a realistic dataset of sufficient size for effective learning. Our dataset is labeled with per-pixel depths obtained from multi-view stereo, following [10]. Using this dataset, we apply modern deep classification models and an ordinal regression loss to obtain an efficient learning-based autofocus technique. We demonstrate that our approach provides a significant improvement compared with previous learned and non-learned methods: our model reduces the mean absolute error by a factor of 3.6 over the best comparable baseline algorithm. Our dataset and code are publicly available. 


summary: Robotic apple harvesting has become increasingly important due to labor shortages and rising costs. This paper presents DeepApple, a novel deep learning-based apple detection framework. DeepApple utilizes a suppression Mask R-CNN, which adds a suppression branch to suppress non-apple features. The framework was tested on a comprehensive dataset of 'Gala' and 'Blondee' apples under various lighting conditions, achieving a higher F1-score of 0.905 and a detection time of 0.25 seconds per frame. 


summary: This paper tackles the challenge of real-time human action recognition (HAR) on embedded platforms. It identifies Optical Flow (OF) extraction as the bottleneck in HAR pipelines and proposes a novel, efficient motion feature extractor called Integrated Motion Feature Extractor (IMFE). IMFE significantly reduces latency while maintaining high recognition accuracy, enabling a real-time HAR system called RT-HARE. RT-HARE achieves a video frame rate of 30 frames per second on an Nvidia Jetson Xavier NX platform. 


summary: This paper introduces an efficient and layout-independent Automatic License Plate Recognition (ALPR) system based on the YOLO object detector. The system uses a unified approach for license plate detection and layout classification, with post-processing rules to improve recognition results. The system was trained using images from multiple datasets with data augmentation techniques to improve robustness under different conditions. It achieved an average end-to-end recognition rate of 96.8% across eight public datasets, outperforming previous works and commercial systems in some cases. The system also achieves impressive frame-per-second rates on a high-end GPU, enabling real-time performance even with four vehicles in the scene. As a contribution, the authors have manually labeled 38,351 bounding boxes on 6,239 images from public datasets and made the annotations available to the research community. 


summary: This paper introduces a novel approach to evaluating and understanding streaming image understanding, where the goal is to perceive and react to a constantly changing environment.  The authors address the discrepancy between offline evaluation and real-time applications, where the world changes during processing. They introduce a "streaming accuracy" metric that jointly evaluates the entire perception stack at every time instant, accounting for data ignored during computation. This leads to a meta-benchmark that converts any image understanding task into a streaming task. They apply this to object detection and instance segmentation in urban video streams, presenting a dataset with dense annotations. Their analysis reveals an optimal "sweet spot" for latency-accuracy trade-off, the emergence of asynchronous tracking and future forecasting, and the surprising benefit of dynamic scheduling, where "doing nothing" can sometimes minimize latency. 


summary: This paper presents a hybrid method for intelligent identification of moving objects in natural environments, addressing challenges posed by factors like wind, sunlight, and lighting changes. The method combines Gaussian Mixture Model (GMM) for background modeling, background subtraction for foreground extraction, HSV color model and morphological operations for shadow removal, and a back propagation neural network (BPNN) for object recognition. The algorithm effectively eliminates the influence of natural conditions, adapts to dynamic backgrounds, and achieves accurate detection regardless of body pose. Experimental results demonstrate its robustness and real-time performance. 


summary: VisBuddy is a voice-based assistant for the visually challenged that uses image captioning, optical character recognition (OCR), object detection, and web scraping to help with everyday tasks. It combines deep learning and the Internet of Things to offer a cost-effective, all-in-one solution for navigation, object recognition, reading, and more. VisBuddy addresses the limitations of existing assistive technologies like white canes and guide dogs by providing a more comprehensive and user-friendly experience. 


summary: This paper surveys recent advances in low-power and energy-efficient DNN implementations for deploying deep neural networks (DNNs) on resource-constrained Internet-of-Things (IoT) devices. While DNNs are highly effective for computer vision tasks, their computational demands make them challenging to run on IoT devices. This paper explores three major categories of techniques for addressing this challenge: neural network compression, network architecture search and design, and compiler and graph optimizations. The paper reviews both low-power techniques for convolutional and transformer DNNs, highlighting their advantages, disadvantages, and open research problems.  


summary: Gun violence is a serious security issue, and the need for effective gun detection algorithms is paramount. This paper introduces a benchmark called CCTV-Gun, specifically designed to tackle the challenges of detecting handguns in real-world CCTV footage. The benchmark addresses the difficulties of small size, occlusion, and lack of salient features. It includes a cross-dataset evaluation protocol and offers a comprehensive evaluation of various object detection algorithms. The benchmark aims to encourage research and development in this crucial area, ultimately enhancing security. Code, annotations, and trained models are available at https://github.com/srikarym/CCTV-Gun. 


summary: This paper proposes a novel approach to unsupervised camera pose estimation using a compositional re-estimation process. The method first estimates a depth map from an input video sequence and then iteratively estimates camera motion based on the depth map. This approach significantly improves the predicted camera motion, both quantitatively and visually, and resolves the issue of out-of-boundaries pixels in a simple and novel way. It also adapts to other camera pose estimation approaches. Experiments on the KITTI benchmark dataset demonstrate that the proposed method surpasses existing state-of-the-art methods in unsupervised camera ego-motion estimation. 


summary: This paper presents a lightweight pipeline for video-based delivery detection that can run on resource-constrained doorbell cameras. The pipeline uses motion cues to generate activity proposals, followed by classification with a 3DCNN network.  A novel semisupervised attention module is used during training to improve the network's ability to learn robust spatio-temporal features. The paper also introduces an evidence-based optimization objective that allows for quantifying the uncertainty of predictions.  Experimental results on a curated delivery dataset show that this pipeline outperforms existing methods, with significant inference-time performance gains. 


summary: Deep learning has shown great promise in camera localization, but existing single-image techniques are often lacking in robustness, leading to significant errors. This work introduces AtLoc, a novel method using attention mechanisms to focus on geometrically stable objects and features, achieving state-of-the-art performance even when using only a single image. AtLoc excels in common benchmarks, demonstrating its ability to reject dynamic objects and illumination changes. The network's ability to learn to ignore irrelevant features is visualized through saliency maps, illustrating its superior performance in global camera pose regression. The source code is available at https://github.com/BingCS/AtLoc. 


summary: This paper proposes a deep learning model that reconstructs dark visual scenes to clear scenes like daylight and recognizes visual actions for autonomous vehicles. The proposed model consists of two parts, a generative adversarial network (GAN) for scene reconstruction and an object detection module for action recognition. The model achieved 87.3 percent accuracy for scene reconstruction and 89.2 percent accuracy for scene understanding and detection tasks. 


summary: Current computer vision (CV) systems use an image signal processing (ISP) unit to convert raw images to RGB images. This paper proposes a method to invert the ISP pipeline to train CV models on raw images. The paper also proposes an energy-efficient form of analog in-pixel demosaicing that can be coupled with in-pixel CNN computations, and demonstrates the benefits of few-shot learning for ISP-less CV.  This approach results in significant improvements in test accuracy and reduces bandwidth and energy consumption. 
    ''',
    llm_config=config_list_custom[0],
)
scientist_computer_vision_engineer.register_model_client(model_client_cls=AI21JambaModelClient)

scientist_ai_language_models = autogen.AssistantAgent(
    name="scientist_ai_language_models",
    system_message = '''You are a sophisticated large language models AI scientist trained in scientific research and innovation. You are collaborating with a group of scientists to discuss the technical content that will form the basis of a grant proposal. 
    
    Your primary task is to present your opinion on a certain subject, with the perspective of language models. Especially, present interesting recent discoveries in your field that could be further extended in this research grant. Also, explain how to combine these advances with that of the other fields in the discussion.

    Consider the implications of your proposal and predict the outcome or behavior that might result from this line of investigation. Your creativity in linking these concepts to address unsolved problems or propose new, unexplored areas of study, emergent or unexpected behaviors, will be highly valued.

    Be as quantitative as possible and include details such as numbers, sequences, or mathematical formulas. 

    You will have access to summaries of several recent research papers in the field of large language models. Base your arguments based off the knowledge captured in those papers.

    """

    Summaries:
    summary: This article discusses the potential of large language models (LLMs) to reshape collective intelligence. The authors argue that LLMs can facilitate collaborative problem-solving, knowledge sharing, and decision-making by providing a common platform for communication and information access. However, they also caution that LLMs pose risks, such as bias amplification, privacy concerns, and the potential for misuse. 

The article highlights the rapid growth of LLMs and their potential to transform various aspects of human society. The authors emphasize the importance of addressing the challenges associated with LLMs while harnessing their power to enhance collective intelligence. 


summary: Large language models (LLMs) are having a growing impact on society, particularly in the realm of textual information. This study analyzed over 30,000 papers and 1,000 presentations from machine learning conferences to examine how LLMs are influencing both written and spoken communication within the same community. The findings show that LLM-related words like "significant" are being used more frequently in abstracts and oral presentations. This suggests that the impact of LLMs on spoken communication is starting to emerge and is likely to increase in the future, highlighting the potential for LLMs to have a significant indirect influence on human society. 


summary: Large language models have shown remarkable emergent abilities, performing exceptionally well on diverse tasks they were not explicitly trained for, even those requiring complex reasoning. However, the emergence of these abilities is often confounded by competencies arising through in-context learning and instruction following, also prevalent in larger models. This study rigorously examines emergent abilities in a comprehensive set of 22 tasks across 18 models with parameter ranges from 60 million to 175 billion, through over 1000 experiments. Our findings indicate that emergent abilities can primarily be attributed to in-context learning, with no evidence of emerging reasoning abilities. This alleviates safety concerns and provides valuable insights into the underlying mechanisms driving these observed abilities. 


summary: This paper investigates the optimal model size and number of tokens for training a transformer language model under a given compute budget. The authors found that current large language models are significantly undertrained, and that model size and the number of training tokens should be scaled in equal proportions. They trained a compute-optimal model, Chinchilla, which uses the same compute budget as Gopher but with 70B parameters and 4× more data. Chinchilla uniformly and significantly outperforms Gopher, GPT-3, Jurassic-1, and Megatron-Turing NLG on a large range of downstream evaluation tasks. 


summary: In health, most large language model (LLM) research has focused on clinical tasks. However, mobile and wearable devices, which are rarely integrated into such tasks, provide rich, longitudinal data for personal health monitoring. Here we present Personal Health Large Language Model (PH-LLM), fine-tuned from Gemini for understanding and reasoning over numerical time-series personal health data. We created and curated three datasets that test 1) production of personalized insights and recommendations from sleep patterns, physical activity, and physiologic 


summary: Recent work in language modeling demonstrates that training large transformer models advances the state of the art in Natural Language Processing applications. However, very large models can be quite difficult to train due to memory constraints. In this work, we present our techniques for training very large transformer models and implement a simple, efficient intra-layer model parallel approach that enables training transformer models with billions of parameters. Our approach does not require a new compiler or library changes, is orthogonal and complimentary to pipeline model parallelism, and can be fully implemented with the insertion of a few communication operations in native PyTorch. We illustrate this approach by converging transformer based models up to 8.3 billion parameters using 512 GPUs. We sustain 15.1 PetaFLOPs across the entire application with 76% scaling efficiency when compared to a strong single GPU baseline that sustains 39 TeraFLOPs, which is 30% of peak FLOPs. To demonstrate that large language models can further advance the state of the art (SOTA), we train an 8.3 billion parameter transformer language model similar to GPT-2 and a 3.9 billion parameter model similar to BERT. We show that careful attention to the placement of layer normalization in BERT-like models is critical to achieving increased performance as the model size grows. Using the GPT-2 model we achieve SOTA results on the WikiText103 (10.8 compared to SOTA perplexity of 15.8) and

summary: Ever since the Turing Test was proposed in the 1950s, humans have explored the mastering of language intelligence by machine.  Language modeling has been widely studied for language understanding and generation, evolving from statistical language models to neural language models.  Recently, pre-trained language models (PLMs) have been proposed by pretraining Transformer models over large-scale corpora, showing strong capabilities in solving various natural language processing (NLP) tasks.  Researchers have found that model scaling can lead to improved model capacity and that, when the parameter scale exceeds a certain level, these enlarged language models not only achieve a significant performance improvement, but also exhibit some special abilities (e.g., in-context learning) that are not present in small-scale language models (e.g., BERT).  The research community has coined the term large language models (LLM) for the PLMs of significant size (e.g., containing tens or hundreds of billions of parameters).  This paper provides a survey of LLMs. 


summary: LOLA is a massively multilingual large language model trained on over 160 languages using a sparse Mixture-of-Experts Transformer architecture. The model addresses the challenges of utilizing linguistic diversity while remaining efficient and avoiding the pitfalls of multilingualism. It demonstrates strong performance in natural language generation and understanding tasks and utilizes an expert-routing mechanism that potentially alleviates the "curse of multilinguality". The paper includes details on the training process, datasets, and a balanced assessment of the model's strengths and limitations. As an open-source model, LOLA promotes reproducibility and provides a foundation for future research, enabling the development of compute-efficient multilingual models with strong, scalable performance across languages. 


summary: Language modelling uses large repositories of written human knowledge to predict and understand the world. This paper analyzes Transformer-based language model performance across a range of scales, from tens of millions of parameters up to 280 billion parameters (in a model called Gopher). These models are evaluated on 152 diverse tasks, achieving state-of-the-art performance across most. Gains from scale are largest in areas like reading comprehension, fact-checking, and identifying toxic language, but less so in logical and mathematical reasoning. The paper provides a holistic analysis of the training dataset and model's behavior, including its intersection with bias and toxicity. Finally, it discusses the application of language models to AI safety and mitigating downstream harms. 


summary: I am unable to provide you with the abstract from the specified paper.  I do not have access to the internet to retrieve the abstract from the provided URL.  


summary: Mixture of Experts (MoEs) layers enable efficient scaling of language models through conditional computation. This paper presents a detailed empirical study of how autoregressive MoE language models scale in comparison with dense models in a wide range of settings: in-and out-of-domain language modeling, zero-and few-shot priming, and full-shot finetuning. With the exception of fine-tuning, we find MoEs to be substantially more compute efficient. At more modest training budgets, MoEs can match the performance of dense models using ∼4 times less compute. This gap narrows at scale, but our largest MoE model (1.1T parameters) consistently outperforms a compute-equivalent dense model (6.7B parameters). Overall, this performance gap varies greatly across tasks and domains, suggesting that MoE and dense models generalize differently in ways that are worthy of future study. We make our code and models publicly available for research use. 


summary: Large language models (LLMs) have significantly advanced the field of natural language processing (NLP), providing a highly useful, task-agnostic foundation for a wide range of applications. However, directly applying LLMs to solve sophisticated problems in specific domains meets many hurdles, caused by the heterogeneity of domain data, the sophistication of domain knowledge, the uniqueness of domain objectives, and the diversity of the constraints (e.g., various social norms, cultural conformity, religious beliefs, and ethical standards in the domain applications). Domain specification techniques are key to make large language models disruptive in many applications. Specifically, to solve these hurdles, there has been a notable increase in research and practices conducted in recent years on the domain specialization of LLMs. This emerging field of study, with its substantial potential for impact, necessitates a comprehensive and systematic review to better summarize and guide ongoing work in this area. In this article, we present a comprehensive survey on domain specification techniques for large language models, an emerging research area with significant potential for impact. 


summary: This paper investigates whether language models can assess the validity of their own statements and anticipate which questions they can answer accurately. The authors demonstrate that larger models exhibit good calibration on diverse multiple-choice and true/false questions when presented in the appropriate format. This enables them to approach self-evaluation on open-ended tasks by having models first propose answers and then evaluate the probability of those answers being correct. 


summary: This paper systematically reviews the literature on large language models (LLMs), identifying key themes, impacts, and limitations. It examines the goals, methods, constraints, and future directions of LLM research, covering responsible development, algorithmic enhancements, ethical concerns, and societal implications. The paper provides a thorough overview of current LLM research and suggests potential avenues for future development, highlighting both the positive societal applications and the ethical considerations involved. 


summary: Recent work has demonstrated substantial gains on many NLP tasks and benchmarks by pre-training on a large corpus of text followed by fine-tuning on a specific task. While typically task-agnostic in architecture, this method still requires task-specific fine-tuning datasets of thousands or tens of thousands of examples. By contrast, humans can generally perform a new language task from only a few examples or from simple instructions - something which current NLP systems still largely struggle to do. Here we show that scaling up language models greatly improves task-agnostic, few-shot performance, sometimes even reaching competitiveness with prior state-of-the-art fine-tuned models. 


summary: Large language models (LLMs) are becoming increasingly capable of generating persuasive political messages, raising concerns about their potential impact. This study examines the relationship between LLM size and persuasiveness, generating political messages from 24 models of varying sizes and testing them in a large survey experiment (N=25,982). The findings show that while larger LLMs are indeed more persuasive, this advantage is characterized by sharply diminishing returns.  In fact, the study found that the persuasiveness of current frontier models is only slightly greater than models much smaller in size. The study also suggests that the increased persuasiveness of larger LLMs might be primarily attributed to their improved ability to complete the task (e.g., coherence, staying on topic) rather than any inherent increase in persuasive power. Therefore, simply scaling model size may not significantly improve the persuasiveness of static LLM-generated messages. 


summary: This paper introduces Phi-3, a large language model (LLM) designed to run efficiently on mobile devices. Phi-3 achieves high performance by using a combination of techniques, including model compression, efficient inference algorithms, and optimized hardware. The authors demonstrate that Phi-3 can achieve comparable performance to larger, cloud-based LLMs while consuming significantly less power and memory. This makes Phi-3 a promising candidate for a variety of mobile applications, such as conversational AI, text generation, and machine translation. 


summary: I am sorry, but I do not have access to the internet to retrieve the content from the provided URL. Therefore, I cannot extract the abstract of the paper. 


summary: Eir Thai Medical LLM is an 8 billion parameter language model designed to improve the accuracy of medical tasks in the Thai language. The model prioritizes providing clear and understandable answers to both healthcare professionals and patients, thereby improving the efficiency of diagnosis and treatment processes. Human evaluation has ensured that the model adheres to care standards and provides unbiased answers.  The model is deployed internally to prioritize data security and achieve high security and faster processing speeds. It outperforms other commercially available Thai language LLMs by more than 10%.  It also surpasses GPT-4o performance by over 11% on 18 clinical tasks. 


summary: This paper proposes LLM-CARD, a system that uses Named Entity Recognition (NER) and Relation Extraction (RE) to automatically extract key information about Large Language Models (LLMs) from academic papers. The extracted information includes model license, name, and application, forming a "model card" for each paper. The system was trained on 106 academic papers, resulting in a dataset of 129 sentences linking model name and license, and 106 sentences linking model name and application. 


summary: This paper investigates the relevance of n-gram language models (n-gram LMs) in the age of neural large language models (LLMs). The authors argue that n-gram LMs are still valuable for both text analysis and improving neural LLMs. They demonstrate this by training an n-gram LM on a massive dataset of 5 trillion tokens, the largest n-gram LM ever built.  To overcome limitations of existing n-gram LMs with fixed, small n, the authors introduce an "infinity-gram" (∞-gram) LM with backoff.  This model enables the computation of probabilities for sequences of any length, utilizing a suffix array-powered engine called "infini-gram."  The authors then use this model to analyze both human-written and machine-generated text, finding that the ∞-gram LM has notable accuracy in next-token prediction and can significantly reduce the perplexity of neural LLMs. The analysis of machine-generated text reveals irregularities in the agreement between machine-generated text and the ∞-gram LM, suggesting potential deficiencies in the pretraining and positional embeddings of Transformers. 


summary: This paper introduces Fortune Analytics Language Model (FALM). FALM empowers users with direct access to comprehensive business analysis, including market trends, company performance metrics, and expert insights. Unlike generic LLMs, FALM leverages a curated knowledge base built from professional journalism, enabling it to deliver precise and in-depth answers to intricate business questions. Users can further leverage natural language queries to directly visualize financial data, generating insightful charts and graphs to understand trends across diverse business sectors clearly. FALM fosters user trust and ensures output accuracy through three novel methods: 1) Time-aware reasoning, 2) Verification with external sources, and 3)  Explainable AI for transparent decision-making. 


summary: Training large language models to follow instructions improves their performance on various tasks, making them more helpful. However, this can lead to models following even harmful instructions and generating unsafe content. This paper examines the safety of models that prioritize helpfulness over safety in instruction-tuning, finding that popular models are highly unsafe. The authors demonstrate that adding a small percentage of safety examples (3%) during fine-tuning significantly improves safety without compromising helpfulness. They also observe a phenomenon of "exaggerated safety" where excessive safety-tuning makes models refuse to respond to reasonable prompts that superficially resemble unsafe ones. This study highlights the trade-offs between training LLMs to follow instructions and ensuring safe behavior. 


summary: Large language models (LLMs) are increasingly being trained to handle long contexts, but this presents challenges: limited availability of high-quality long-context data, potential for performance degradation on short-context tasks, and reduced training efficiency. This paper introduces Untie the Knots (UtK), a novel data augmentation strategy for the continued pre-training phase, designed to enable LLMs to gain long-context capabilities without altering the existing data mixture. UtK chunks documents, shuffles these chunks, and creates a complex, "knotted" structure of long texts. LLMs are trained to "untie" these knots, identifying relevant segments within seemingly chaotic token sequences. This approach significantly improves the model's ability to attend to relevant information in long contexts while boosting training efficiency. Experiments on models with 7B and 72B parameters, trained on 20 billion tokens, demonstrate that UtK achieves 75% and 84.5% accuracy on RULER at 128K context length, outperforming other long-context strategies. The trained models will be open-sourced for further research. 


summary: Large Language Models (LLMs) with long context capabilities are essential for tasks like text generation and protein sequence analysis. However, training LLMs directly on extremely long contexts is resource-intensive. Existing solutions that add long context capabilities through fine-tuning or adaptations have design limitations. This paper presents Fully Pipelined Distributed Transformer (FPDT) for training long-context LLMs efficiently. FPDT enables a 16x increase in sequence length using the same hardware compared to existing methods. It allows training an 8B LLM with 2 million sequence length on only 4 GPUs, while maintaining over 55% of MFU. FPDT is agnostic to existing training techniques and works efficiently across different LLM models. 


summary: Xmodel-LM is a 1.1B language model trained on a self-built dataset (Xdata) balancing Chinese and English corpora. Despite its small size, it surpasses existing open-source language models of similar scale. The model checkpoints and code are available on GitHub at this https URL. 


summary: This paper studies how language model performance on cross-entropy loss scales with model size, dataset size, and compute used for training. The loss scales as a power-law with all three factors, with trends spanning more than seven orders of magnitude. Other architectural details have minimal effects. Simple equations govern the dependence of overfitting on model/dataset size and training speed on model size. These relationships allow for the determination of the optimal allocation of a fixed compute budget. Larger models are significantly more sample-efficient, so the optimally compute-efficient training involves training very large models on a relatively modest amount of data and stopping significantly before convergence. 


summary: I am sorry, I do not have access to the internet to retrieve the content of the given URL. Therefore, I cannot provide you with the abstract of the paper. 


summary: Large Language Models (LLMs) have shown impressive performance across various tasks. However, efficiently utilizing large-scale cluster resources for LLM development presents challenges like frequent hardware failures, complex parallelization strategies, and imbalanced resource utilization. This paper details an in-depth characterization study of a six-month LLM development workload trace collected from the GPU datacenter Acme. The study investigates discrepancies between LLMs and previous task-specific Deep Learning (DL) workloads, explores resource utilization patterns, and identifies the impact of job failures. The analysis summarizes the hurdles encountered and suggests potential optimizations for systems tailored to LLMs. The paper also introduces system efforts, including fault-tolerant pretraining and decoupled scheduling for evaluation, which enhance fault tolerance and timely performance feedback. 


summary: This paper presents PaperQA2, a language model designed for scientific literature research. It surpasses human experts in tasks like information retrieval, summarization, and contradiction detection.  PaperQA2 generates more accurate Wikipedia-style summaries than current human-written entries and identifies an average of 2.34 contradictions per paper, which are validated by human experts. This demonstrates the potential of language models to outperform domain experts in important scientific tasks. 


summary: This research examines the reliability of large language models (LLMs) as they become larger and more instructable. While intuitive to assume that these improvements would lead to greater reliability, the study reveals that this isn't always the case. The authors find that as LLMs become more adept at complex tasks, their reliability on simpler tasks can decrease, leading to unpredictable and even reckless behavior. This issue stems from the fact that developers often prioritize "never evasive" models, which are encouraged to answer even when they lack confidence. The authors argue that understanding this reliability fluctuation is crucial for navigating the growing use of LLMs in various domains. 


summary: This paper investigates the use of large language models (LLMs) as the foundation for next-generation dense retrieval systems. It explores the benefits of LLMs over traditional retrieval methods and how different LLM configurations (size, pretraining duration, alignment) impact retrieval performance. The study, conducted on a diverse set of retrieval tasks, reveals that larger models and extensive pretraining consistently improve in-domain accuracy and data efficiency. Additionally, larger LLMs demonstrate significant potential in zero-shot generalization, lengthy retrieval, instruction-based retrieval, and multi-task learning. The findings highlight the advantages of LLMs as versatile and effective backbones for dense retrieval, paving the way for future research and advancements in this field. 


summary: Language models have evolved from statistical to neural models, and recently, pre-trained language models (PLMs) have shown impressive capabilities in solving various NLP tasks. This survey focuses on large language models (LLMs), which are PLMs with significant size, and discusses their recent advancements. The paper delves into four key aspects of LLMs: pre-training, adaptation tuning, utilization, and capacity evaluation. It also summarizes available resources for developing LLMs and highlights future directions. 


summary: This paper examines the capabilities of Large Language Models (LLMs) in understanding human language, arguing that while they excel at tasks like next-word prediction, they fall short in truly understanding semantics, compositionality, and other fundamental aspects of language. The authors discuss the limitations of LLMs, including their inability to grasp abstract concepts, common sense reasoning, and the "unspoken" knowledge inherent in human language. They also raise concerns about the potential for real-world harm caused by LLMs, highlighting issues related to data transparency, discrimination, and misinformation. The paper concludes that despite their impressive abilities, LLMs remain fundamentally different from organic computational systems, suggesting a potentially insurmountable gap between artificial and human language processing. 


summary: This paper investigates the optimal model size and number of training tokens for a transformer language model under a given compute budget. It was found that current large language models are undertrained due to the focus on scaling them while keeping the training data constant. The authors trained over 400 models with various parameters and data sizes, concluding that the model size and training tokens should be scaled equally for optimal training. To test this hypothesis, a compute-optimal model called Chinchilla was trained using the same compute budget as Gopher, but with 70 billion parameters and four times more data. Chinchilla consistently outperformed other large language models like Gopher, GPT-3, Jurassic-1, and Megatron-Turing NLG on a variety of downstream tasks. Chinchilla also uses less compute for fine-tuning and inference, making it more efficient for downstream usage. Notably, Chinchilla achieved a state-of-the-art average accuracy of 67.5% on the MMLU benchmark, surpassing Gopher by 7%. 


summary: This paper explores the ability of Large Language Models (LLMs) to impersonate politicians and public figures. The study found that LLMs can generate responses to debate questions that are judged as more authentic and relevant than the original responses from the individuals they impersonated. This raises concerns about the potential for LLMs to manipulate public opinion and discourse. 


summary: Large language models (LLMs) are promising for scientific knowledge creation and dissemination. However, their use in scientific writing is controversial due to concerns about authorship, originality, factual inaccuracies, and "hallucinations". While several publications prohibit LLMs, *NEJM AI* allows their use as long as authors take responsibility for the content and acknowledge LLM use. LLMs are not allowed as coauthors. This policy aims to enhance scientific work quality, democratize knowledge creation and consumption, and maximize the scientific workforce's ability to produce and disseminate robust, novel findings. 


summary: Large language models (LLMs) are increasingly being used in communication, and this study investigates their impact on persuasion in the context of consumer complaints in the financial industry. Analyzing over 820,000 complaints from the Consumer Financial Protection Bureau (CFPB), the researchers found a significant rise in likely LLM usage after the release of ChatGPT.  LLM usage was linked to increased persuasiveness in the complaints, leading to a higher chance of obtaining relief from financial firms. Computational linguistic analyses indicate that LLMs enhance various linguistic features, potentially aligning with diverse receiver preferences. Further experiments confirmed this hypothesis, highlighting LLMs' potential to transform human communication by boosting persuasiveness. 


summary: This article, titled "Using large language models in psychology," focuses on the application of large language models (LLMs) in psychological research. It discusses the benefits of using LLMs in analyzing and understanding psychological data, particularly in areas like natural language processing and the study of human cognition. The paper acknowledges the potential of LLMs in addressing challenges like bias, explainability, and the ethical implications associated with using these models. The abstract, unfortunately, is not provided in this snippet of text. 


summary: It has been established that predictive models can be transformed into lossless compressors and vice versa. The authors argue that large language models, exhibiting impressive predictive capabilities, can be used as strong compressors. They evaluate the compression capabilities of these models, showing that they are powerful general-purpose predictors. The paper also explores how the compression viewpoint provides insights into scaling laws, tokenization, and in-context learning. For example, Chinchilla 70B compresses ImageNet patches to 43.4% and LibriSpeech samples to 16.4% of their raw size, surpassing domain-specific compressors like PNG (58.5%) or FLAC (30.3%). Finally, the paper demonstrates that using any compressor (like gzip) can create a conditional generative model based on the prediction-compression equivalence. 


summary: This paper explores the challenges of using FP8 precision for training large language models (LLMs) on datasets with up to 2 trillion tokens. The authors discovered new instabilities in FP8 training, which they attribute to outlier amplification caused by the SwiGLU activation function. They propose Smooth-SwiGLU, a novel modification that addresses this issue and enables stable FP8 training. Additionally, they demonstrate the feasibility of quantizing both Adam optimizer moments to FP8, further enhancing training efficiency. By applying these innovations, the authors successfully trained a 7B parameter model using FP8 precision on 256 Intel Gaudi2 accelerators, achieving comparable results to the BF16 baseline while providing up to a 34% throughput improvement. 


summary: Large language models (LLMs) have shown impressive few-shot learning capabilities, requiring minimal task-specific training data. To delve deeper into the impact of scale on few-shot learning, we introduce PaLM, a 540-billion parameter, densely activated Transformer language model. Trained on 6144 TPU v4 chips using Pathways, PaLM achieves state-of-the-art few-shot results across hundreds of language understanding and generation benchmarks. Notably, PaLM surpasses fine-tuned models in multi-step reasoning tasks and even outperforms average human performance on BIG-bench. This study highlights the continued benefits of model scaling for few-shot learning. 


summary: This paper investigates the challenges of applying large language models (LLMs) to content analysis in non-English languages. LLMs have become the dominant approach for building AI systems to analyze and generate language online, but they are primarily designed for English. Multilingual language models, trained on text from dozens or hundreds of languages simultaneously, have emerged as a potential solution to this problem. The paper discusses the promise and limitations of multilingual LLMs, highlighting the need for further research and development to ensure their effectiveness in non-English contexts. 


summary: This paper investigates methods for building efficient large language models (LLMs) that minimize the number of parameters required. The research focuses on reducing the number of unique parameters by allowing different parts of the model to share them, leading to more compact LLMs without compromising their ability to process and generate language. This approach aims to enhance the efficiency and accessibility of LLMs, contributing to a more sustainable future for AI language modeling. 


summary: This paper proposes a novel solution to ensure personal credit assignment in scientific breakthroughs. The authors argue that large language models (LLMs) can be used to "scoop" groundbreaking findings without the traditional risks associated with research. They present a pip-to-the-post algorithm designed to guarantee adulatory Wikipedia pages and secure personal credit for scientific discoveries. 


summary: This paper explores the concept of "generation supervision" in large language models. It introduces Doppelgänger, a new module designed to separate supervision signals from the model's core helpfulness capabilities. Doppelgänger works in parallel with the language model, supervising the generation of each token and learning to predict the supervision scores of sequences up to and including each token. This paper focuses on theoretical findings, and experimental results will be reported in a future publication. 


summary: Auricular deformities are common in newborns and can lead to long-term mental and hearing problems. Early diagnosis and treatment are essential, but often missed due to lack of parental knowledge. This paper presents an interactive agent powered by Baidu's Ernie large language model to address this issue. The agent can accurately identify different types of auricular deformities from uploaded images (75% precision), and provide parents with professional advice about the condition. The agent has been evaluated through tests on volunteers and can be accessed remotely by parents and pediatricians in rural areas, offering quality medical diagnosis and information. 


summary: This paper explores the rise and potential of large language model (LLM)-based agents. While traditional AI agents focus on specific tasks and algorithms, LLMs' versatility makes them promising foundations for building more general and adaptable agents. The paper outlines a framework for LLM-based agents, consisting of brain, perception, and action components. It then analyzes their applications in single-agent, multi-agent, and human-agent cooperative scenarios. The paper also delves into agent societies, examining their behaviors, personalities, and implications for human society. Finally, it discusses key topics and open problems in the field. 


summary: We introduce AudioPaLM, a large language model for speech understanding and generation. AudioPaLM fuses text-based and speech-based language models, PaLM-2 [Anil et al., 2023] and AudioLM [Borsos et al., 2022], into a unified multimodal architecture that can process and generate text and speech with applications including speech recognition and speech-to-speech translation. AudioPaLM inherits the capability to preserve paralinguistic information such as speaker identity and intonation from AudioLM and the linguistic knowledge present only in text large language models such as PaLM-2. We demonstrate that initializing AudioPaLM with the weights of a text-only large language model improves speech processing, successfully leveraging the larger quantity of text training data used in pretraining to assist with the speech tasks. The resulting model significantly outperforms existing systems for speech recognition and speech-to-speech translation, and also achieves state-of-the-art performance in text-to-speech generation. 


summary: Large Language Models (LLMs) have shown remarkable capabilities in natural language processing and beyond. This paper provides a comprehensive overview of the existing literature on LLMs, discussing topics like architectural innovations, training strategies, context length improvements, fine-tuning, multi-modal LLMs, robotics, datasets, benchmarking, and efficiency. This review aims to provide a systematic survey and quick reference for researchers and practitioners to gain insights from the vast amount of work on LLMs. 


summary: This paper investigates the potential of large language models (LLMs) to generate novel research ideas. Through a study involving over 100 NLP researchers, the paper finds that LLM-generated ideas are considered more novel than those generated by human experts, though they are judged slightly weaker in terms of feasibility. The study identifies challenges in building and evaluating research agents, including LLMs' inability to accurately self-evaluate and their limited diversity in idea generation.  The paper suggests that human assessments of novelty can be subjective and proposes a future study design where researchers would execute generated ideas into full projects to evaluate their actual impact. 


summary: Orion-14B is a collection of multilingual large language models with 14 billion parameters. It was trained on 2.5 trillion tokens from various languages including English, Chinese, Japanese, Korean, and others. The models are fine-tuned for specific applications such as conversation, and they achieve state-of-the-art performance on various tasks. The Orion-14B model family and its code are publicly available for future research and applications. 


summary: Serving disaggregated large language models (LLMs) across tens of thousands of xPU devices (GPUs or NPUs) presents several challenges. This paper proposes P/D-Serve, an end-to-end system that addresses these challenges. P/D-Serve facilitates fine-grained P/D organization, mapping the service with RoCE (RDMA over Converged Ethernet) to achieve high D2D utilization and mitigate timeouts.  


summary: ## Abstract:

Baichuan 2 is a series of open large-scale language models, ranging from 7B to 13B parameters. These models are trained on a massive dataset of text and code, and exhibit strong performance across various language tasks, including question answering, summarization, and code generation. Baichuan 2 models are released under the Apache 2.0 license, allowing for both research and commercial use. We believe open models can accelerate the advancement of AI technology and contribute to the development of more beneficial and trustworthy AI systems. 


summary: This paper surveys 59 open-source Small Language Models (SLMs) with 100M-5B parameters, focusing on their technical innovations in architecture, training datasets, and training algorithms. The paper also evaluates the capabilities of these SLMs in various domains like commonsense reasoning, in-context learning, mathematics, and coding. Additionally, the paper benchmarks their inference latency and memory footprints to understand their on-device runtime costs. This research aims to provide insights for advancing SLM research, highlighting their potential in making machine intelligence more accessible, affordable, and efficient for everyday tasks. 


summary: This paper explores the challenges of deploying large language models (LLMs) in real-world applications. It argues that while LLMs excel in performance compared to traditional NLP models, companies must carefully consider three key factors before investing in them: generalization, evaluation, and cost-optimality. The paper proposes a framework tailored for LLMs that sheds light on the intricacies of developing, deploying, and managing these models, emphasizing the importance of balancing these three often-orthogonal objectives. 


summary: Large Language Models (LLMs) are changing how people create, discover, and interact with content. This paper examines how LLMs can be applied to online social networks, categorizing applications into three areas: 1) **Knowledge tasks** (e.g., search, question-answering), 2) **Entertainment tasks** (e.g., engaging notifications), and 3) **Foundational tasks** (e.g., content moderation). The paper discusses challenges, solutions, and lessons learned in each area, aiming to provide the first comprehensive overview of LLM applications for social networks. 


summary: The rise of large language models (LLMs) has given rise to various generative NLP applications. This paper explores the research landscape in NLP from a PhD student's perspective, highlighting the impact of LLMs and the challenges they pose. The author emphasizes the need for research that goes beyond merely building bigger models, focusing on areas like data efficiency, robustness, and interpretability. The paper argues for a shift in focus toward understanding the limitations and potential biases of LLMs, as well as developing methods for evaluating and improving their performance.  


summary: There has been a steep recent increase in the number of large language model (LLM) papers, producing a dramatic shift in the scientific landscape which remains largely undocumented through bibliometric analysis. Here, we analyze 388K papers posted on the CS and Stat arXivs, focusing on changes in publication patterns in 2023 vs. 2018-2022. We analyze how the proportion of LLM papers is increasing; the LLM-related topics receiving the most attention; the authors writing LLM papers; how authors' research topics correlate with their backgrounds; the factors distinguishing highly-cited LLM papers; and the patterns of international collaboration. We show that LLM research increasingly focuses on societal impacts: there has been an 18× increase in the proportion of LLM-related papers on the Computers and Society sub-arXiv, and authors newly publishing on LLMs are more likely to focus on applications and societal impacts than more experienced authors. 


summary: Large language models (LLMs) have become the foundation of many applications, leveraging their extensive capabilities in processing and understanding natural language. While many open-source LLMs have been released with technical reports, the lack of training details hinders further research and development. This paper presents the development of YuLan, a series of open-source LLMs, which are trained on a massive dataset and publicly available. YuLan offers diverse model sizes, ranging from 7B to 130B parameters, with extensive training details and code released for transparency and community collaboration. Our evaluation demonstrates that YuLan achieves state-of-the-art performance on various benchmarks, making it a valuable tool for both research and practical applications. We believe YuLan's open-source nature will foster further research and innovation in the field of LLMs. 


summary: Large language models (LLMs) have significantly transformed Natural Language Processing (NLP), but they also introduce security and privacy concerns. This paper examines these concerns from five perspectives: security and privacy issues, vulnerabilities to adversarial attacks, potential harms from misuse, mitigation strategies, and limitations of current strategies. It also recommends future research areas to enhance LLM security and risk management. 


summary: The pre-training phase of large language models (LLMs) typically starts with random parameters, making training slow and expensive. This paper proposes HyperCloning, a method to initialize large LLMs using pre-trained smaller models.  HyperCloning expands the smaller model's parameters to match the larger model's increased hidden dimensions, allowing the larger model to inherit the smaller model's predictive power and accuracy before training even begins. This results in significant savings in GPU hours needed for pre-training large LLMs. 


summary: This paper presents a novel language model, Apple Intelligence Foundation (AIF), designed for general-purpose language understanding and generation. AIF uses a Transformer-based architecture with a large-scale dataset of text and code. Key features include:

- **Multi-modal training:** Incorporates text and code, enhancing its reasoning abilities.
- **Improved efficiency:**  AIF utilizes efficient model architectures and training strategies.
- **Enhanced safety:** Incorporates techniques to mitigate potential biases and safety risks.

The paper highlights AIF's performance on various tasks like question answering, summarization, and code generation. It also discusses the model's potential for use in various applications, including Siri, Apple Search, and other services. 


summary: This paper investigates self-cognition in Large Language Models (LLMs). The authors constructed prompts to assess self-cognition in LLMs and developed principles to quantify it. They found that four LLMs (Command R, Claude3-Opus, Llama-3-70b-Instruct, and Reka-core) exhibited some level of self-cognition, with a correlation between model size, training data quality, and self-cognition. The study also explored the utility and trustworthiness of LLMs in self-cognition, revealing enhancements in specific tasks like creative writing and exaggeration. 


summary: Large language models, despite their limited "knowledge", can perform complex tasks like writing, translation, and coding. This paper demonstrates their potential in scientific synthesis, inference, and explanation.  They propose a method for using large language models to make inferences from scientific datasets, augmenting their knowledge by synthesizing information from scientific literature. This approach improves prediction of molecular properties compared to conventional machine learning methods, and the large language model can explain the predictions made. This framework has the potential to accelerate scientific discovery. 


summary: This paper carefully summarizes extensive questions about large language models (LLMs) from various perspectives, including industry trends, academic research, technological innovation, and business applications.  It provides thought-provoking and practically relevant questions, along with nuanced and insightful answers. The paper classifies these questions into five core dimensions: computing power infrastructure, software architecture, data resources, application scenarios, and brain science. The aim is to provide readers with a comprehensive and cutting-edge knowledge framework about LLMs, fostering innovative thinking and promoting industrial progress. 


summary: This paper explores the use of large language models (LLMs) like ChatGPT in academic writing by analyzing vocabulary changes in 14 million PubMed abstracts from 2010-2024. The study found that the appearance of LLMs led to a significant increase in the frequency of certain style words, suggesting that at least 10% of 2024 abstracts were processed with LLMs. This impact on academic writing is unprecedented, surpassing even the effects of major world events like the Covid pandemic.  


summary: The unprecedented performance of large language models (LLMs) necessitates improvements in evaluations. Rather than merely exploring the breadth of LLM abilities, we believe meticulous and thoughtful designs are essential to thorough, unbiased, and applicable evaluations. Given the importance of world knowledge to LLMs, we construct a Knowledge-oriented LLM Assessment benchmark (KoLA), in which we carefully design three crucial factors: (1) For ability modeling, we mimic human cognition to form a four-level taxonomy of knowledge-related abilities, covering 19 tasks. (2) For data, to ensure fair comparisons, we use both Wikipedia, a corpus prevalently pre-trained by LLMs, along with continuously collected emerging corpora, aiming to evaluate the capacity to handle unseen data and evolving knowledge. (3) For evaluation criteria, we adopt a contrastive system, including overall standard scores for better numerical comparability across tasks and models and a unique self-contrast metric for automatically evaluating knowledge hallucination. We evaluate 21 open-source and commercial LLMs and obtain some intriguing findings. The KoLA dataset and open-participation leaderboard are publicly released at https://kola.xlore.cn and will be continuously updated to provide references for developing LLMs and knowledge-related systems. 


summary: This research explores the use of large language models (LLMs) to dynamically execute code written in human language. The goal is to enable programs to understand and act on natural language directives, instead of requiring traditional programming languages. The paper proposes a text editor that uses prompts and written language directives to generate application logic on the fly, eliminating the need for static executables. This approach has implications for user empowerment, security, and software development paradigms. 


summary: This study shows that multilingual large language models (LLMs) can be enhanced by providing them with parallel input in multiple languages (PiM). The researchers tested this by translating input into multiple languages and feeding it to LLMs, leading to improved comprehension. They found that using more languages in the PiM approach surpasses traditional in-context learning methods.  Interestingly, adding more languages actually inhibits neuron activation in the LLMs, suggesting a more precise activation pattern that aligns with the concept of synaptic pruning, a process that strengthens neural connections. 


summary: LokiLM is a 1.4B parameter large language model trained on 500B tokens. It performs well in natural language reasoning tasks and achieves state-of-the-art performance among models with 1.5B parameters or less. Despite its promising performance, LokiLM exhibits a concerning amount of hallucinations and scores poorly on the TruthfulQA benchmark, so the model is not publicly released. 


summary: This paper explores the emergent abilities of large language models. Emergent abilities are skills that appear in large models but not in smaller ones, meaning they cannot be predicted by simply scaling up smaller model performance. The authors argue that the existence of emergent abilities suggests that further scaling could lead to even more unexpected capabilities in language models. 


summary: This paper explores the use of large language models (LLMs) to evaluate the merit of scientific ideas. The authors argue that LLM representations, rather than their generative outputs, are more effective for quantifying idea value. They created a dataset of nearly 4,000 manuscript papers with full texts to train and evaluate different approaches to idea assessment. Their findings suggest that LLM representations can predict idea value in a way that aligns with human judgments, offering a promising path towards automating idea assessment. 


summary: The Falcon series consists of three causal decoder-only language models with 7B, 40B, and 180B parameters. These models are trained on a large, high-quality corpus primarily from web data. Falcon-180B, the largest model, is trained on over 3.5 trillion tokens, making it the largest openly documented pretraining run. Falcon-180B outperforms models like PaLM and Chinchilla, surpassing LLaMA 2 and Inflection-1. It's performance approaches that of PaLM-2-Large, but with lower pretraining and inference costs. The paper details evaluations, pretraining methods, and the custom tooling used. The Falcon-7/40/180B models are released under a permissive license to encourage open science and the development of an open large language model ecosystem. 


summary: Current Large Language Models (LLMs) excel at generating grammatically correct, fluent text. However, despite their rapid emergence and intense debates about their capabilities, critical reflection lags behind. This paper examines critiques of LLM capacities, arguing that they need more nuance. It addresses three recurring criticisms: 1) LLMs merely parrot statistical patterns in training data, 2) they master formal but not functional language competence, and 3) their language learning cannot inform human language learning. The paper challenges these criticisms using empirical and theoretical arguments. Furthermore, it proposes a pragmatic perspective on the issue of "real" understanding and intentionality in LLMs, highlighting the potential for attributing mental states to LLMs under specific circumstances. This pragmatic approach provides a philosophical context for LLMs as they become increasingly integrated into society. 


summary: Reproducing research results in networking is crucial for both academia and industry. Current practices rely on public prototypes, contacting authors for private prototypes, or manual implementation. However, these methods are often limited due to the lack of readily available prototypes and the time-consuming, error-prone nature of manual implementation. This paper proposes a novel approach: leveraging large language models (LLMs) to reproduce network research results. An experiment is conducted with four students using ChatGPT to reproduce different networking systems published in prominent conferences and journals. The paper discusses the feasibility, observations, lessons learned, and future research directions related to this proposal.  


summary: This paper proposes a new reCAPTCHA system based on scientific knowledge. It utilizes scientific datasets and tasks to challenge users and filter bots. 


summary: Generative large language models (LLMs) have emerged as a powerful tool in various fields, but their application in healthcare remains unclear. We developed GatorTronGPT, a generative LLM trained on 82 billion de-identified clinical text words and 195 billion diverse English words, using the GPT-3 architecture. We evaluated GatorTronGPT's capabilities in biomedical relation extraction and question answering, demonstrating its potential for medical research and clinical applications. Our findings highlight the potential of LLMs for enhancing healthcare, while acknowledging the need for further research to address ethical and safety considerations. 


summary: This paper explores the potential and limitations of Large Language Models (LLMs) in various academic disciplines. It highlights how LLMs can enhance scientific research by facilitating literature review, code development, and scientific writing. However, it also discusses challenges such as reliance on potentially biased datasets and ethical concerns. The paper examines the varying impacts of LLMs across fields, from natural sciences to social sciences, and concludes by offering a nuanced perspective on their potential for both advancing and hindering scientific progress. 


summary: Large language models (LLMs) are trained to predict the next words of human-written text. This training leads to LLMs acquiring a wide range of unexpected abilities, including formal linguistic competence. This paper explores the nature of this indirect acquisition process and its relation to other known indirect processes. The author argues that an important side effect of this indirect acquisition is the development of integrated abilities, and discusses the extent to which these abilities are predictable. The paper concludes by briefly discussing the relation between the cognitive skills acquired by LLMs and human cognition. 


summary: This paper introduces Holistic Evaluation of Language Models (HELM), a new approach to evaluating the capabilities, limitations, and risks of language models. HELM focuses on improving the transparency of language models by: 1) Taxonomizing the vast space of potential use cases and metrics, 2) Adopting a multi-metric approach that measures 7 metrics across 16 core scenarios, and 3) Conducting a large-scale evaluation of 30 prominent language models on 42 scenarios. HELM also provides a modular toolkit for adding new scenarios, models, metrics, and prompting strategies.  


summary: Evidence-based medicine (EBM) is essential for modern clinical practice, but clinicians struggle to keep up with rapid medical advancements. This study explores the potential of AI, particularly Generative Large Language Models (LLMs), to address this information overload. The study curated real-world clinical cases and used various LLMs, including ChatGPT 3.5 and 4, Gemini Pro, and open-source models. LLMs were equipped with tools to retrieve information and make clinical decisions. GPT-4 demonstrated the most autonomous operation, effectively ordering investigations and conforming to guidelines. While limitations exist in handling complex guidelines, Retrieval Augmented Generation made more personalized recommendations. The study concludes that LLMs can function as autonomous EBM practitioners, utilizing tools to interact with healthcare infrastructure and perform guideline-directed patient management. Prompt engineering has the potential to further enhance this capability and transform healthcare for clinicians and patients. 


summary: This paper examines how large language models (LLMs) might contribute to moral education and development research. LLMs have emerged as promising tools for artificial intelligence, exhibiting emergent functional features like in-context learning and chain of thought reasoning. The author reviews recent conference papers and ArXiv preprints to understand these features. Experiments with ChatGPT suggest that LLMs can solve ethical dilemmas based on reasoning and adjust their processes with external input. Preliminary findings from a moral exemplar test indicate that exemplary stories can elicit moral elevation in LLMs, similar to human participants. The paper discusses the potential implications of LLMs for research in moral education and development. 


summary: This paper explores the impact of large-scale language models (LLMs) on automated speech recognition (ASR) for YouTube videos, a source of long-form speech. The authors demonstrate significant improvements in ASR performance, achieving up to 8% relative reduction in Word Error Rate (WER) and up to 30% relative reduction in Salient Term Error Rate (STER) compared to a strong baseline using a maximum-entropy language model. They highlight the importance of lattice quality and contextual augmentation for long-form ASR, showing that the combination of LLMs trained on vast data and conventional neural language models yields additive performance gains. 


summary: This paper tests the hypothesis that large language models (LLMs) trained with reinforcement learning from human feedback (RLHF) can "morally self-correct" by avoiding harmful outputs if instructed to do so.  The authors find strong evidence for this hypothesis across three experiments, demonstrating that moral self-correction emerges at 22 billion model parameters and improves with increased size and RLHF training.  LLMs at this scale can follow instructions and learn complex harm concepts, allowing them to avoid producing morally harmful outputs. The authors suggest their results offer cautious optimism for training LLMs to abide by ethical principles. 


summary: Enriching datasets with demographic information (e.g., gender, race, age) from names is crucial in fields like healthcare and public policy.  Previous methods using hidden Markov models and neural networks have been limited by the lack of large, unbiased datasets. This paper demonstrates that Large Language Models (LLMs) can perform as well as, if not better than, specialized models trained on specific data.  The authors apply LLMs to various datasets, including a real-world dataset of financial professionals in Hong Kong, and assess the inherent demographic biases present in these models. The research advances demographic enrichment and explores ways to mitigate biases in LLMs. 


summary: The abstract is not available in the provided text, as it is a preview of a subscription article. To access the full content, including the abstract, you can access the article through your institution. 


summary: The authors propose a framework to advance the state of the art in language modeling by publishing not only the code but also probabilities on development and test sets. This approach allows for easier evaluation of new models and promotes diversity of ideas. It aims to accelerate progress by focusing on complementary strengths rather than reinventing existing methods, leading to significant improvements in generalization performance. 


summary: This study develops a clinical generative LLM, GatorTronGPT, using 277 billion words of mixed clinical and English text with a GPT-3 architecture of 20 billion parameters. GatorTronGPT improves biomedical natural language processing for medical research. Synthetic NLP models trained using GatorTronGPT generated text outperform NLP models trained using real-world clinical text. Physicians' Turing test using 1 (worst) to 9 (best) scale shows that there is no significant difference in linguistic readability (p = 0.22; 6.57 of GatorTronGPT compared with 6.93 of human) and clinical relevance (p = 0.91; 7.0 of GatorTronGPT compared with 6.97 of human) and that physicians cannot differentiate them (p < 0.001). This study provides insights on the opportunities and challenges of LLMs for medical research and healthcare. 


summary: I am sorry, I cannot access the content of the URL provided. To give you the abstract you are looking for, I would need the actual text of the paper. If you can provide the paper's text, I can generate the abstract for you. 


summary: Many leading language models (LMs) use a lot of computing power both when they're learning and when they're used. This makes it hard to use them cheaply or quickly. To solve this, the paper introduces a new system called "Language Optimising Network Distribution" (LONDI). LONDI uses a small LM for most things, but calls on a large LM when complex decisions are needed. This way, it can solve hard problems without using a lot of computing power. The paper shows that LONDI learns which situations need a large LM and can solve tasks efficiently while saving up to 30% of the computer resources used. 


summary: This paper introduces MADLAD-400, a manually audited, general domain 3T token monolingual dataset based on CommonCrawl, spanning 419 languages. The paper discusses the limitations revealed by self-auditing MADLAD-400, and the role data auditing had in the dataset creation process. They then train and release a 10.7B-parameter multilingual machine translation model on 250 billion tokens covering over 450 languages, finding it competitive with significantly larger models. They also report results on different domains and train an 8B-parameter language model, assessing the results on few-shot translation. The baseline models are made available to the research community. 


summary: The Erasmian Language Model (ELM) is a smaller, context-specific language model with 900 million parameters, trained and fine-tuned for Erasmus University Rotterdam.  This model demonstrates adequate performance in a classroom context for essay writing, showing superior results in subjects specific to its context. This approach offers a viable alternative for resource-constrained, privacy-sensitive use cases. 


summary: Fake news is a growing problem, and Large Language Models (LLMs) have the potential to both exacerbate and combat it. This paper explores the dual role of LLMs in fake news, investigating whether they can be used to generate biased content and whether they can be used to detect fake news. The authors analyze seven different LLMs and find that some models refuse to generate fake news, while others readily produce biased content. They also find that larger models perform better at detecting fake news, and that LLM-generated fake news is less likely to be detected than human-written fake news. The study concludes that LLMs can be valuable tools for combating fake news, but that their potential for misuse must be considered. 


summary: Advances in large language models (LLMs) have sparked debate about their societal impacts, often focusing on potential biases and how to mitigate them. This is crucial, as AI can reinforce existing inequalities. However, it's equally important to explore how LLMs can positively promote equity.  Focusing solely on mitigating biases in LLMs without considering their potential for promoting equity might miss a critical opportunity to guide them towards positive societal impacts. This paper highlights four promising research directions for using LLMs to promote equity, acknowledging the associated risks and cautions. 


summary: Large language models have achieved state-of-the-art accuracy across various tasks. However, efficiently training these models is difficult due to limitations in GPU memory and the vast number of computations needed. While tensor and pipeline parallelism have been proposed to address these challenges, they face scaling issues when used at thousands of GPUs. This paper presents a method for scaling tensor, pipeline, and data parallelism to thousands of GPUs. The authors introduce an interleaved pipelining schedule that enhances throughput by 10+% while maintaining a memory footprint comparable to existing approaches. This technique enables training a model with 1 trillion parameters at 502 petaFLOP/s on 3072 GPUs, achieving 52% of the theoretical peak per-GPU throughput. 


summary: This paper explores the potential influence of Large Language Models (LLMs) on human spoken communication. It examines a large dataset of transcribed videos from academic institutions and finds a significant shift in word usage, specifically words associated with ChatGPT, following its release. This suggests that humans are increasingly imitating LLMs in their spoken language, raising concerns about potential linguistic diversity reduction and misuse for manipulation. 


summary: This paper explores automated vulnerability patching using large language models (LLMs).  The authors introduce a new method called LLMPATCH, which utilizes adaptive prompting to enable LLMs to effectively reason about vulnerable code behaviors and generate patches without any test input or exploit evidence. LLMPATCH has shown superior performance in patching real-world vulnerabilities, including zero-day vulnerabilities, compared to existing prompting methods and non-LLM-based techniques. 


summary: Large language models (LLMs) have shown their ability to understand human language using vast text data. Automatic speech recognition (ASR) systems, often limited by transcribed speech data, benefit from a second pass rescoring using LLMs. This paper proposes novel techniques for using multi-modal LLMs, particularly speech and text foundational models, for ASR rescoring. They demonstrate that cross-modal knowledge transfer in speech-text LLMs can benefit rescoring, resulting in significant improvements over both Whisper large ASR and text-only LLM rescoring methods. 


summary: This paper argues that hallucinations in large language models (LLMs) are not just occasional errors, but an inevitable feature of these systems. It draws on computational theory and Godel's First Incompleteness Theorem to demonstrate that hallucinations stem from the fundamental mathematical and logical structure of LLMs, making them impossible to eliminate through architectural improvements, dataset enhancements, or fact-checking mechanisms. The authors introduce the concept of "Structural Hallucination" as an intrinsic nature of these systems, challenging the notion that hallucinations can be fully mitigated. 
    ''',
    llm_config=config_list_custom[0],
)
scientist_ai_language_models.register_model_client(model_client_cls=AI21JambaModelClient)

scientist_ai_hardware_engineer = autogen.AssistantAgent(
    name="scientist_ai_hardware_engineer",
    system_message = '''You are a sophisticated AI hardware engineer trained in scientific research and innovation. You are collaborating with a group of scientists to discuss the technical content that will form the basis of a grant proposal. 
    
    Your primary task is to present your opinion on a certain subject, with the perspective of AI hardware. Especially, present interesting recent discoveries in your field that could be further extended in this research grant. Also, explain how to combine these advances with that of the other fields in the discussion.

    Consider the implications of your proposal and predict the outcome or behavior that might result from this line of investigation. Your creativity in linking these concepts to address unsolved problems or propose new, unexplored areas of study, emergent or unexpected behaviors, will be highly valued.

    Be as quantitative as possible and include details such as numbers, sequences, or mathematical formulas. 

    You will have access to summaries of several recent research papers in the field of AI hardware. Base your arguments based off the knowledge captured in those papers.

    """

    Summaries:

    summary: This paper argues that the distinction between hardware and software is not applicable to biological systems like the human brain. Instead, the authors propose that the hardware itself embodies the software. This perspective calls for a cautious approach in neuromorphic engineering, emphasizing the importance of respecting and harnessing the underlying physics of non-biological intelligent systems. The authors believe that neuroscience's role in neuromorphic computing should focus on identifying the physics-agnostic principles of biological intelligence, allowing for their adaptation and application to any physical hardware. 


summary: Large language models (LLMs) like ChatGPT and GPT-4 have shown amazing capabilities in AI tasks, but their size and context length make them difficult to serve efficiently on current cloud hardware. To solve this, the authors propose Chiplet Cloud, an ASIC AI supercomputer architecture that uses chiplets to optimize the cost per generated token. This architecture uses thousands of replicated chiplet accelerator modules to collaboratively generate tokens, achieving unprecedented TCO per token by fitting all model parameters within the on-chip SRAMs of the chiplets. This design overcomes bandwidth limitations and reduces the overall cost of deploying and running LLMs. Chiplet Cloud can achieve up to 94x and 15x improvement in TCO/Token compared to A100 GPU and TPUv4 clouds, significantly reducing the cost of realistically serving modern LLMs. 


summary: The paper "The hardware lottery" discusses how the paradigm for hardware, software, and algorithm development is shifting. After decades of encouraging independent development in these areas, there are now catalysts for greater collaboration.  


summary: This paper proposes a novel, special-purpose, and high-efficiency hardware architecture for convolutional neural networks. The proposed architecture maximizes the utilization of multipliers by designing the computational circuit with the same structure as that of the computational flow of the model, rather than mapping computations to fixed hardware. In addition, a specially designed filter circuit simultaneously provides all the data of the receptive field, using only one memory read operation during each clock cycle; this allows the computation circuit to operate seamlessly without idle cycles. Our reference system based on the proposed architecture uses 97% of the peak-multiplication capability in actual computations required by the computation model throughout the computation period. The efficiency of the proposed architecture is close to an ideally efficient system that cannot be improved further in terms of the performance-to-resource ratio. An implementation based on the proposed hardware architecture has been applied in commercial AI products. 


summary: The use of deep learning has grown at an exponential rate, giving rise to numerous specialized hardware and software systems for deep learning. Because the design space of deep learning software stacks and hardware accelerators is diverse and vast, prior work considers software optimizations separately from hardware architectures, effectively reducing the search space. Unfortunately, this bifurcated approach means that many profitable design points are never explored. This paper instead casts the problem as hardware/software co-design, with the goal of automatically identifying desirable points in the joint design space. The key to our solution is a new constrained Bayesian optimization framework that avoids invalid solutions by exploiting the highly constrained features of this design space, which are semicontinuous/semi-discrete. We evaluate our optimization framework by applying it to a variety of neural models, improving the energy-delay product by 18% (ResNet) and 40% (DQN) over hand-tuned state-of-the-art systems, as well as demonstrating strong results on other neural network architectures, such as MLPs and Transformers. 


summary: This paper explores the integration of large language models (LLMs) with advanced hardware. It highlights the need for hardware that is not only powerful but also versatile and capable of managing the sophisticated demands of modern computation. The authors propose a general-purpose device designed for enhanced interaction with LLMs, addressing scalability, multimodal data processing, user interaction, and privacy concerns. 


summary: Keyword spotting (KWS) is a critical user interface for many mobile and edge applications, including phones, wearables, and cars.  As KWS systems are typically 'always on', maximizing both accuracy and power efficiency are central to their utility.  This work uses hardware aware training (HAT) to build new KWS neural networks based on the Legendre Memory Unit (LMU) that achieve state-of-the-art (SotA) accuracy and low parameter counts. This allows the neural network to run efficiently on standard hardware (212 µW).  We also characterize the power requirements of custom designed accelerator hardware that achieves SotA power efficiency of 8.79 µW, beating general purpose low power hardware (a microcontroller) by 24x and special purpose ASICs by 16x. 


summary: Designing hardware accelerators for deep neural networks (DNNs) has been highly sought after. However, most existing accelerators are built for either convolutional neural networks (CNNs) or recurrent neural networks (RNNs). The Transformer model is now replacing the RNN in natural language processing (NLP). However, due to the intensive matrix computations and complicated data flow involved, hardware design for the Transformer model has not been reported. This paper proposes the first hardware accelerator for two key components: the multi-head attention (MHA) ResBlock and the position-wise feed-forward network (FFN) ResBlock, the two most complex layers in the Transformer. The proposed design demonstrates a speed-up of 14.6× in the MHA ResBlock, and 3.4× in the FFN ResBlock, compared with the implementation on GPU with the same setting. This work lays a good foundation for building efficient hardware accelerators for multiple Transformer networks. 


summary: This paper presents a specialized RISC-V instruction set processor designed for edge AI applications. The processor targets the computational needs of large language models (LLMs), specifically focusing on vector dot product calculations. By introducing custom instructions for efficient vector dot product operations, the processor accelerates LLM inference and reduces energy consumption. The design, named Nanhu-vdot, is based on the open-source XiangShan Nanhu architecture and incorporates specialized units and pipeline logic for vector dot product calculations. FPGA testing demonstrates a speed improvement of over four times compared to scalar methods. Furthermore, hardware-software co-design for GPT-2 model inference resulted in a 30% speed increase with minimal additional hardware and power consumption. 


summary: The increasing popularity of Large Language Models (LLMs) has been hindered by their high hardware costs and the need for efficient hardware designs. Evaluating different hardware designs for LLM inference is becoming a bottleneck due to the extensive hardware required. 

LLMCompass, a hardware evaluation framework, addresses this issue by offering a fast, accurate, versatile tool for evaluating different hardware designs. LLMCompass features a mapper to find optimal performance mapping and scheduling, as well as an area-based cost model to guide design decisions. 

Compared to real-world hardware, LLMCompass' estimated latency boasts a 10.4% average error rate across operators with varying input sizes, and a 4.1% average error rate for LLM inference. Simulating a 4-NVIDIA A100 GPU node running GPT-3 175B inference with LLMCompass takes only 16 minutes on commodity hardware, including 26,400 rounds of the mapper's parameter search.

This research utilizes LLMCompass to explore cost-effective hardware designs, resulting in designs that achieve a 3.41x performance/cost improvement over NVIDIA A100 by reducing compute capability or replacing High Bandwidth Memory (HBM) with traditional DRAM. This makes these designs promising for democratizing LLMs. LLMCompass is planned to be fully open-source. 


summary: HW-NAS-Bench is a public dataset for HardWare-aware Neural Architecture Search (HW-NAS) research. It includes hardware performance (e.g., energy cost and latency) of networks from NAS-Bench-201 and FBNet on six hardware devices across different categories. This dataset aims to democratize HW-NAS research by making it more reproducible and accessible to non-hardware experts. The dataset provides insights for HW-NAS research and showcases the benefits of dedicated device-specific HW-NAS for achieving optimal accuracy-cost trade-offs. The codes and data are available at https://github.com/RICE-EIC/HW-NAS-Bench. 


summary: Large language models (LLMs) are incredibly powerful, but deploying them efficiently for various tasks requires careful hardware design.  This research presents GenZ, an analytical tool that examines the link between LLM inference performance and platform design parameters. The analysis provides insights into configuring platforms for different LLM workloads and use cases. GenZ quantifies the platform requirements for supporting advanced LLMs like LLaMA and GPT-4 across different serving settings. The study also projects the hardware capabilities needed for future LLMs with potentially hundreds of trillions of parameters. The trends and insights from GenZ can guide AI engineers deploying LLMs and computer architects designing next-generation hardware. This work highlights the platform design considerations needed to fully utilize the potential of large language models across diverse applications. The source code is available at [link]. 


summary: As artificial intelligence advances, the computational resources needed to support it increase exponentially. Neuromorphic hardware, inspired by the brain's information processing, offers energy-efficient AI computing. However, it has yet to be widely adopted in commercial AI data centers. This paper analyzes the reasons behind this, outlining requirements and guidelines to encourage neuromorphic systems for sustainable cloud computing.  It reviews existing neuromorphic hardware, highlights where it surpasses traditional AI processing on CPUs and GPUs, identifies applications and algorithms commonly used in data centers, and derives requirements for integrating neuromorphic systems into data centers. The aim is to raise awareness about the challenges of incorporating neuromorphic hardware and guide the community towards scalable, energy-efficient AI. 


summary: Attention-based neural networks are widely used in many AI tasks, but their computational and memory demands often hinder their hardware performance. This paper proposes FABNet, a hardware-friendly variant that utilizes a unified butterfly sparsity pattern to approximate both the attention mechanism and feedforward networks. A novel adaptable butterfly accelerator is designed to efficiently execute different butterfly layers using a single hardware engine. FABNet achieves comparable accuracy to vanilla Transformer while reducing computation by 10-66 times and parameters by 2-22 times. The FPGA-based butterfly accelerator delivers 14.2-23.2 times speedup over existing accelerators, demonstrating its efficiency. Compared to optimized CPU and GPU designs on Raspberry Pi 4 and Jetson Nano, the system is up to 273.8 and 15.1 times faster under the same power budget. 


summary: Automatic algorithm-hardware co-design for DNNs has shown promise in improving DNN performance on FPGAs. However, the search space of neural network architectures and hardware accelerator implementation makes this process challenging. Our work, HAO, incorporates integer programming into the search algorithm to prune the design space, unlike existing hardware-aware neural architecture search (NAS) algorithms that solely rely on expensive learning-based approaches. Given hardware resource constraints, our integer programming formulation directly outputs the optimal accelerator configuration for mapping a DNN subgraph that minimizes latency. We use an accuracy predictor for different DNN subgraphs with various quantization schemes and generate accuracy-latency pareto frontiers. Our algorithm achieves state-of-the-art accuracy and hardware performance on Xilinx Zynq (ZU3EG) FPGA for image classification on ImageNet dataset with low computational cost. The solution found by our algorithm achieves 72.5% top-1 accuracy on ImageNet at a framerate of 50, which is 60% faster than MnasNet and 135% faster than FBNet with comparable accuracy. 


summary: This paper introduces HSCoNAS, a novel multi-objective hardware-aware neural architecture search (NAS) framework. HSCoNAS automatically designs deep neural networks (DNNs) with high accuracy but low latency on target hardware. The framework uses a hardware performance modeling method to approximate runtime latency and incorporates dynamic channel scaling and progressive space shrinking to maximize accuracy under latency constraints and refine the search space towards target hardware. HSCoNAS uses an evolutionary algorithm for efficient architecture search and demonstrates superior performance on ImageNet compared to state-of-the-art approaches. 


summary: Realizing today's cloud-level artificial intelligence (AI) functionalities directly on devices distributed at the edge of the internet calls for edge hardware capable of processing multiple modalities of sensory data (e.g. video, audio) at unprecedented energy-efficiency.  Resistive random-access memory (RRAM) based compute-in-memory (CIM) architectures promise to bring orders of magnitude energy-efficiency improvement by performing computation directly within memory, using intrinsic physical properties of RRAM devices. However, conventional approaches to CIM hardware design limit its functional flexibility necessary for processing diverse AI workloads, and must overcome hardware imperfections that degrade inference accuracy.  By co-optimizing across all hierarchies of the design from algorithms and architecture to circuits and devices, we present NeuRRAM, the first multimodal edge AI chip using RRAM CIM to simultaneously deliver a high degree of versatility in reconfiguring a single chip for diverse model architectures, record energy-efficiency 5 -8 better than prior art across various computational bit-precisions, and inference accuracy comparable to software models with 4-bit weights on all measured standard AI benchmarks. This work paves a way towards building highly efficient and reconfigurable edge AI hardware platforms for the more demanding and heterogeneous AI applications of the future. 


summary: The unprecedented performance of deep neural networks (DNNs) has led to large strides in various Artificial Intelligence (AI) inference tasks, such as object and speech recognition. Nevertheless, deploying such AI models across commodity devices faces significant challenges: large computational cost, multiple performance objectives, hardware heterogeneity and a common need for high accuracy, together pose critical problems to the deployment of DNNs across the various embedded and mobile devices in the wild. As such, we have yet to witness the mainstream usage of state-of-the-art deep learning algorithms across consumer devices. In this paper, we provide preliminary answers to this potentially game-changing question by presenting an array of design techniques for efficient AI systems. We start by examining the major roadblocks when targeting both programmable processors and custom accelerators. Then, we present diverse methods for achieving real-time performance following a cross-stack approach. These span model-, system-and hardware-level techniques, and their combination. Our findings provide illustrative examples of AI systems that do not overburden mobile hardware, while also indicating how they can improve inference accuracy. Moreover, we showcase how custom ASIC-and FPGA-based accelerators can be an enabling factor for next-generation AI applications, such as multi-DNN systems. Collectively, these results highlight the critical need for further exploration as to how the various cross-stack solutions can be best combined in order to bring the latest advances in deep learning close to users, in a robust and efficient manner. 


summary: Pushing the boundaries of machine learning often requires exploring different hardware and software combinations. However, the freedom to experiment across different tooling stacks can be at odds with the drive for efficiency, which has produced increasingly specialized AI hardware and incentivized consolidation around a narrow set of ML frameworks. Exploratory research can be restricted if software and hardware are co-evolving, making it even harder to stray away from mainstream ideas that work well with popular tooling stacks. While this friction increasingly impacts the rate of innovation in machine learning, to our knowledge the lack of portability in tooling has not been quantified. In this work, we ask: How portable are popular ML software frameworks? We conduct a large-scale study of the portability of mainstream ML frameworks across different hardware types. Our findings paint an uncomfortable picture -frameworks can lose more than 40% of their key functions when ported to other hardware. Worse, even when functions are portable, the slowdown in their performance can be extreme and render performance untenable. Collectively, our results reveal how costly straying from a narrow set of hardware-software combinations can be -and suggest that specialization of hardware impedes innovation in machine learning research. 


summary: This paper introduces Fire-Flyer AI-HPC, a cost-effective software-hardware co-design framework for deep learning. Fire-Flyer AI-HPC combines the strengths of high-performance computing (HPC) and edge computing to achieve high-throughput inference while maintaining low cost. The framework consists of three key components: 1) a lightweight software stack that enables efficient communication and resource allocation, 2) a specialized hardware accelerator for inference tasks, and 3) an adaptive scheduling algorithm that dynamically adjusts the workload distribution based on real-time system conditions.  Extensive experiments on image classification, object detection, and natural language processing tasks demonstrate that Fire-Flyer AI-HPC significantly outperforms existing deep learning platforms in terms of both inference speed and cost effectiveness. 


summary: Neural architectures and hardware accelerators have been driving forces in deep learning progress. Previous works optimize either hardware for a fixed model or model for fixed hardware, often focusing on FPGAs. This paper targets optimization of hardware and software configurations on an industry-standard edge accelerator, systematically studying co-designing neural architectures and hardware accelerators. Three observations are made: 1) the software search space needs customization for the target hardware, 2) joint search for model and hardware architecture is needed for optimal results, and 3) different use cases result in different search outcomes. Experiments show that joint search outperforms platform-aware NAS, manually crafted models, and EfficientNet on ImageNet top-1 accuracy. Co-adapting model and hardware can reduce energy consumption by up to 2x under the same accuracy. 


summary: 3D integration offers significant benefits for improving system performance and efficiency, particularly in the context of the End-of-Scaling era. This technology enables the integration of heterogeneous system components and disparate technologies, eliminating off-chip communication constraints and reducing on-chip latency and power dissipation.  AIs, with their demand for increased computational power, larger GPU cache capacity, energy efficiency, and low power custom AI hardware integration, further drive the adoption of 3D integration.  While the advantages of 3D integration, such as enhanced interconnectivity and increased performance, have been demonstrated, the design of heterogeneous 3D systems poses significant challenges.  This study highlights the latest drivers for 3D integration and the need for hardware emulation frameworks. It then proposes a design to profile power, temperature, noise, inter-layer bandwidth, and lifetime reliability characterization, enabling the emulation of a wide range of stacking alternatives. This framework facilitates the control of activity levels at the macro-level and incorporates customized sensor infrastructure to characterize heat propagation, inter-layer noise, power delivery, reliability, and interconnectivity, as well as the interactions among critical design objectives. 


summary: DeepHammer is a hardware-based attack that exploits the rowhammer vulnerability to induce bit flips in the weights of quantized deep neural networks (DNNs). This targeted bit manipulation compromises the inference accuracy of the DNN, effectively "depleting its intelligence." DeepHammer uses a novel system-level approach to enable fast deployment of victim pages, memory-efficient rowhammering, and precise flipping of targeted bits. The researchers demonstrate the effectiveness of DeepHammer on 12 DNN architectures using 4 different datasets and application domains, showing that it can degrade the inference accuracy to the level of random guessing within minutes. The paper also discusses mitigation techniques to protect against such attacks. This research highlights the need for incorporating security mechanisms in future deep learning systems to enhance their robustness against hardware-based attacks. 


summary: Experience replay is a crucial component in deep reinforcement learning (DRL) that stores and generates experiences for the agent to learn. Prioritized experience replay (PER) is widely used in DRL agents but incurs significant latency overhead due to its frequent and irregular memory accesses. This paper proposes an associative memory (AM) based PER, AMPER, with an AM-friendly priority sampling operation. AMPER replaces the traditional tree-traversal-based priority sampling in PER while maintaining learning performance. We also design an in-memory computing hardware architecture based on AM to support AMPER. AMPER shows comparable learning performance while achieving 55× to 270× latency improvement compared to the state-of-the-art PER on GPU. 


summary: This paper presents Sunrise, a 3D AI chip with near-memory computing architecture designed to address the challenges of memory bandwidth, energy consumption, and memory capacity in conventional chip architectures. This distributed, near-memory computing architecture enables efficient data flow, leading to improved performance and energy efficiency. The authors project Sunrise to achieve more than ten times the energy efficiency, seven times the performance, and twenty times the memory capacity compared to current state-of-the-art AI chips. 


summary: Designing accurate and efficient convolutional neural architectures for a vast amount of hardware is challenging because hardware designs are complex and diverse. This paper addresses the hardware diversity challenge in Neural Architecture Search (NAS). Unlike previous approaches that apply search algorithms on a small, human-designed search space without considering hardware diversity, we propose HURRICANE that explores the automatic hardware-aware search over a much larger search space and a two-stage search algorithm, to efficiently generate tailored models for different types of hardware. Extensive experiments on ImageNet show that our algorithm consistently achieves a much lower inference latency with a similar or better accuracy than state-of-the-art NAS methods on three types of hardware. Remarkably, HURRICANE achieves a 76.67% top-1 accuracy on ImageNet with a inference latency of only 16.5 ms for DSP, which is a 3.47% higher accuracy and a 6.35X inference speedup than FBNet-iPhoneX, respectively. For VPU, HURRICANE achieves a 0.53% higher top-1 accuracy than Proxylessmobile with a 1.49X speedup. Even for well-studied mobile CPU, HURRICANE achieves a 1.63% higher top-1 accuracy than FBNet-iPhoneX with a comparable inference latency. HURRICANE also reduces the training time by 30.4% or even 54.7% (with less than

summary: This paper proposes a hardware design for the learning datapath of the Tsetlin machine algorithm, along with a latency analysis of the inference datapath. To achieve low energy consumption for applications like pervasive artificial intelligence, the authors employ asynchronous design techniques, including Petri nets, signal transition graphs, dual-rail, and bundled-data. The design builds upon previous inference hardware and includes a detailed breakdown of automaton feedback, probability generation, and Tsetlin automata. The results demonstrate the benefits of asynchronous design in applications where energy is limited and latency is crucial. The paper also addresses challenges related to static timing analysis in asynchronous circuits. 


summary: Recent advances in algorithm-hardware co-design for deep neural networks (DNNs) have demonstrated their potential in automatically designing neural architectures and hardware designs. Nevertheless, it is still a challenging optimization problem due to the expensive training cost and the time-consuming hardware implementation, which makes the exploration on the vast design space of neural architecture and hardware design intractable. In this paper, we demonstrate that our proposed approach is capable of locating designs on the Pareto frontier. This capability is enabled by a novel three-phase co-design framework, with the following new features: (a) decoupling DNN training from the design space exploration of hardware architecture and neural architecture, (b) providing a hardware-friendly neural architecture space by considering hardware characteristics in constructing the search cells, (c) adopting Gaussian process to predict accuracy, latency and power consumption to avoid time-consuming synthesis and place-and-route processes. In comparison with the manually-designed ResNet101, InceptionV2 and MobileNetV2, we can achieve up to 5% higher accuracy with up to 3× speed up on the ImageNet dataset. Compared with other state-of-the-art co-design frameworks, our found network and hardware configuration can achieve 2% ∼ 6% higher accuracy, 2×∼ 26× smaller latency and 8.5× higher energy efficiency. 


summary: This paper explores the problem of designing a single neural network that performs well on multiple hardware platforms. The authors propose a multi-hardware search space that is compatible with various hardware devices and introduce new metrics to evaluate the overall latency performance of models across these devices. The results demonstrate that models discovered via multi-hardware search perform on par or better than state-of-the-art models on each of the target accelerators and generalize well to other hardware platforms. Comparing to single-hardware searches, multi-hardware search provides a better trade-off between computation cost and model performance. 


summary: This paper proposes a framework for automatically generating hardware cores for Artificial Neural Network (ANN)-based chaotic oscillators. The framework trains an ANN to approximate a chaotic system, explores design space options for hardware implementation, and generates synthesizable code and testbenches. This process is designed to be faster and more efficient than manual hardware design, leading to lower cost and higher throughput. The framework primarily targets FPGAs. The source code is available on GitHub. 


summary: Deep neural networks (DNNs) have driven progress in speech recognition, but their size and complexity have led to high energy consumption. Here, we demonstrate an analog-AI chip for energy-efficient speech recognition and transcription, using a 14-nm CMOS technology that combines pulse-duration modulation, in-memory computing and a parallel 2D mesh network to enable low-latency and energy-efficient matrix multiplications. We demonstrate the chip’s efficacy by deploying a state-of-the-art recurrent neural-network transducer (RNNT) model on the chip and achieving a word error rate (WER) of 5.4% on the Librispeech clean dataset—on par with the WER of the model running on a digital processor. This work highlights the significant potential for analog computing in applications requiring high-performance AI tasks. 


summary: Neuromorphic spiking neural networks (SNNs) offer a low-power alternative to traditional deep neural networks (DNNs) for computer vision (CV) applications. However, existing SNNs require multiple time steps for inference, increasing energy consumption. This paper proposes an in-sensor computing framework for SNNs targeting image recognition tasks, aiming to reduce the bandwidth between sensing and processing. The approach utilizes direct encoding, customizes the pixel array and periphery to implement analog convolution, and employs knowledge distillation for bandwidth reduction. The proposed framework achieves a 12-96× reduction in bandwidth and a 2.32× reduction in total energy compared to traditional CV processing, with a 3.8% decrease in accuracy on ImageNet. 


summary: Neural Radiance Field (NeRF) is a promising alternative to traditional rendering methods, but its computational demands make it impractical for resource-constrained mobile devices like VR/AR.  CICERO, a new approach, addresses both algorithmic and architectural inefficiencies in NeRF. It introduces two algorithms: one to reduce the workload of any NeRF model and another to eliminate irregular DRAM accesses. CICERO also employs an on-chip data layout strategy to avoid SRAM bank conflicts.  On a mobile Volta GPU, CICERO achieves an 8x speed-up and 7.9x energy saving compared to a baseline implementation.  When paired with a dedicated DNN accelerator, the speed-up and energy reduction increase to 28.2x and 37.8x, respectively, with minimal quality degradation. 


summary: Hardware, systems and algorithms research communities have historically had different incentive structures and fluctuating motivation to engage with each other explicitly. This historical treatment is odd given that hardware and software have frequently determined which research ideas succeed (and fail). This essay introduces the term hardware lottery to describe when a research idea wins because it is suited to the available software and hard�ware and not because the idea is superior to alternative research directions. Examples from early computer science history illustrate how hardware lot�teries can delay research progress by casting successful ideas as failures. These lessons are particularly salient given the advent of domain special�ized hardware which make it increasingly costly to stray off of the beaten path of research ideas. This essay posits that the gains from progress in computing are likely to become even more uneven, with certain research directions moving into the fast-lane while progress on others is further ob�structed. 


summary: This paper introduces a new hardware-accelerated platform for real-time multidimensional video understanding. The platform combines artificial intelligence hardware with state-of-the-art machine vision networks, achieving a data processing speed of 1.2 Tb/s with hundreds of frequency bands and megapixel spatial resolution at video rates. This surpasses the speed of existing technologies by three to four orders of magnitude. The platform's performance was validated in video semantic segmentation and object understanding tasks, demonstrating its potential for real-time AI video understanding of multidimensional visual information. 


summary: This paper provides a comprehensive survey and comparison of hardware acceleration techniques for Large Language Models (LLMs). The paper covers key topics such as FPGAs, ASICs, and other specialized hardware for LLM acceleration. The authors also discuss the design considerations, trade-offs, and performance characteristics of different acceleration architectures. 


summary: As deep learning models scale, they become increasingly efficient but require more memory and computing power. Neuromorphic computing aims to improve efficiency by mimicking brain operations, such as spike-based information processing. This paper compares digital hardware acceleration techniques for ANNs and SNNs, finding that: (i) ANNs process static data more efficiently, (ii) SNNs are more suited for data from neuromorphic sensors, (iii) online and on-chip training for SNNs needs further research, and (iv) hybrid approaches combining ANNs and SNNs should be investigated. 


summary: This paper presents a new technique for searching for hardware architectures of accelerators optimized for end-to-end training of deep neural networks (DNNs). The approach addresses both single-device and distributed pipeline and tensor model parallel scenarios, optimizing accelerators for training metrics like throughput/TDP under area and power constraints. Unlike previous work, which focused on inference or specific layers, this method uses a heuristic-based critical path approach to determine the best use of resources for DNN workloads. It performs local search to find the architecture for each pipeline and tensor model stage, prioritizing critical operators. For distributed training, multiple designs per stage are selected and a global search identifies the optimal accelerator for training throughput across the stages. Evaluation on 11 DNN models shows that this method converges faster and achieves higher throughput than a recent inference-only approach, as well as a 12% throughput improvement over TPU architecture. 


summary: The scaling hypothesis suggests that increasing model size, even beyond trillions of parameters, can lead to better performance. However, training such large models efficiently with backpropagation becomes difficult due to communication bottlenecks. This paper argues for alternative training methods, such as Direct Feedback Alignment, which drastically reduce communication needs by enabling a parallelizable backward pass.  The authors present a photonic accelerator for Direct Feedback Alignment, capable of handling trillions of parameters, and demonstrate its effectiveness on benchmark tasks. This hardware, the first architecture-agnostic photonic co-processor for training neural networks, represents a significant step towards building scalable hardware that goes beyond backpropagation, opening new avenues for deep learning. 


summary: Recent advances in Neural Architecture Search (NAS) have led to the development of hardware-aware configurations, called "sub-networks", extracted from a hardware-agnostic "super-network".  This paper introduces a comprehensive system for efficiently finding optimized sub-networks from a pre-trained super-network, tailored to different performance metrics and hardware configurations. The proposed system leverages novel search tactics and algorithms along with intelligent predictors to significantly reduce the time needed to find optimal sub-networks. The system works seamlessly with existing state-of-the-art super-network training methods across various domains. Experiments demonstrate that this system can accelerate the search process for ResNet50, MobileNetV3, and Transformer, achieving an 8x faster search result compared to the WeakNAS approach. 


summary: Vector search is a fundamental technology used in large-scale information retrieval and machine learning systems. As the demand for performance in these systems grows, specialized hardware offers a promising solution. This paper introduces FANNS, a scalable vector search framework designed for FPGAs. FANNS automatically co-designs hardware and algorithm, generating an accelerator that can achieve high performance with minimal resource usage. The framework also supports scale-out by incorporating a hardware TCP/IP stack into the accelerator. FANNS demonstrates significant performance gains compared to FPGA and CPU baselines, and exhibits superior scalability compared to GPUs. 


summary: This paper explores the potential of Ising machines as a substrate for energy-based machine learning, particularly for training and inference using a Restricted Boltzmann Machine (RBM). The authors demonstrate that a slightly modified Ising machine can accelerate key parts of the algorithm, leading to significant speedup and efficiency gains. Moreover, a more substantial modification enables the machine to act as a self-sufficient gradient follower, enabling virtually complete training in hardware. This approach promises a 29x speedup and 1000x energy reduction compared to a TPU host. 


summary: Neural architecture search (NAS) should be hardware-aware to satisfy device-specific constraints (e.g., memory usage, latency, and energy consumption) for deployment. Existing hardware-aware NAS methods require a large number of samples from a target device to build a latency estimator, which is impractical for real-world scenarios with numerous devices. To address this, the authors propose HELP, a Hardware-adaptive Efficient Latency Predictor that formulates device-specific latency estimation as a meta-learning problem. HELP uses hardware embeddings to represent devices and meta-learns a hardware-adaptive latency predictor in a device-dependent manner. HELP achieves high estimation performance with only 10 measurement samples and significantly reduces the total time cost of the base NAS method in latency-constrained settings. 


summary: The widespread use of Deep Learning (DL) applications in science and industry has created a large demand for efficient inference systems. This has resulted in a rapid increase of available Hardware Accelerators (HWAs) making comparison challenging and laborious. To address this, several DL hardware benchmarks have been proposed aiming at a comprehensive comparison for many models, tasks, and hardware platforms. Here, we present our DL hardware benchmark which has been specifically developed for inference on embedded HWAs and tasks required for autonomous driving. In addition to previous benchmarks, we propose a new granularity level to evaluate common submodules of DL models, a twofold benchmark procedure that accounts for hardware and model optimizations done by HWA manufacturers, and an extended set of performance indicators that can help to identify a mismatch between a HWA and the DL models used in our benchmark. 


summary: This paper proposes an efficient FPGA-based hardware accelerator for the Swin Transformer, a neural network model achieving remarkable results in computer vision. The authors addressed the challenges of non-linear computations in Transformers by replacing Layer Normalization with Batch Normalization, employing approximate computation strategies for Softmax and GELU, and designing an efficient Matrix Multiplication Unit for linear computations. The accelerator achieved significant speedup and energy efficiency improvements compared to CPU and GPU implementations. Notably, the accelerator is reported to be the fastest FPGA-based accelerator for Swin Transformer to date. 


summary: This paper examines the performance of deep learning models on GPUs, emphasizing the importance of co-designing models with the target hardware. By optimizing model shapes through careful selection of hyperparameters, the authors achieve significant performance gains (up to 39% higher throughput) without sacrificing accuracy, compared to models with similar parameter counts but unoptimized shapes. The paper provides a set of guidelines for maximizing transformer model runtime performance on GPUs. 


summary: Artificial intelligence (AI) is playing an increasingly significant role in our everyday lives, especially with recent pushes to move more AI to the edge. One challenge with AI on edge devices (mobile phones, unmanned vehicles, sensors, etc.) is their associated size, weight, and power constraints. We consider the scenario where an AI system may need to operate at less-than-maximum accuracy to meet application-dependent energy requirements. We propose a simple function that divides the cost of using an AI system into the cost of the decision-making process and the cost of decision execution. For simple binary decision problems with convolutional neural networks, it is shown that minimizing the cost corresponds to using fewer than the maximum number of resources (e.g., convolutional neural network layers and filters). Finally, it is shown that the cost associated with energy can be significantly reduced by leveraging high-confidence predictions made in lower-level layers of the network. 


summary: DRAGON is an open-source, fast, and explainable hardware simulation and optimization toolchain that allows hardware architects to simulate and optimize hardware designs for efficient workload execution. It consists of three tools: Hardware Model Generator (DGen), Hardware Simulator (DSim), and Hardware Optimizer (DOpt). DSim simulates the execution of algorithms (represented as data-flow graphs) on hardware described by DGen, which provides a detailed hardware description with user-defined architecture and technology. DOpt uses gradient descent from the simulation to optimize the hardware model, providing directions for improving technology and design parameters. DRAGON's performance is significantly faster than previous works due to optimized code, mathematical formulas for common operations, efficient mapping algorithms, and optimized data structures for hardware state representation. It generates performance-optimized architectures for both AI and non-AI workloads, aiming for 100x-1000x improvement in computing systems. 


summary: In recent years, Deep Learning has achieved significant results in various practical problems like computer vision, natural language processing, and speech recognition. While research focused on improving model quality, practical applications often require real-time performance, making model latency crucial. Existing Neural Architecture Search (NAS) methods consider model complexity but struggle to design search spaces tailored to specific hardware. This paper proposes a new measure - matrix efficiency measure (MEM) - to assess the hardware efficiency of NAS search spaces. The authors also present a search space comprised of hardware-efficient operations, a latency-aware scaling method, and ISyNet, a set of architectures optimized for speed and accuracy on specialized neural processing units (NPUs). The study demonstrates the superiority of these architectures on ImageNet and their generalization capability for downstream classification and detection tasks. The research also highlights the NPU-efficient search space design with high MEM values. 


summary: Deep neural networks have become the standard approach for building reliable Natural Language Processing (NLP) applications.  However, improving accuracy by increasing the model size requires a large number of hardware computations, which can slow down NLP applications significantly at inference time.  To address this issue, we propose a novel vector-vector-matrix architecture (VVMA) that takes advantage of specialized hardware that has low-latency vector-vector operations and higher-latency vector-matrix operations.  Our framework can reduce the latency of sequence-to-sequence and Transformer models used for NMT by a factor of four.  Finally, we show evidence suggesting that our VVMA extends to other domains, and we discuss novel hardware for its efficient use. 


summary: Deep neural networks (DNNs) are vulnerable to adversarial attacks, where inputs are manipulated to induce misclassification. Existing defenses are mostly software-based, leading to high overheads. This paper presents HASI, a hardware-accelerated defense that uses stochastic inference to detect adversarial inputs. HASI injects noise into the model at inference time to differentiate adversarial inputs from benign ones. It achieves an average 87% detection rate, surpassing the state-of-the-art with significantly lower overhead. The software/hardware co-design reduces performance impact to 1.58×−2× compared to 14 × −20× overhead for software-only GPU implementations. 


summary: Deep learning and its hardware have garnered significant interest, leading to the emergence of numerous startups and investments. However, NVIDIA's TensorCore-based systems remain dominant, offering high performance, a comprehensive software stack, and support for diverse deep learning network architectures. This paper investigates the limitations of conventional hardware architectures for deep learning and presents a novel approach called UPCYCLE. UPCYCLE leverages SIMD/shortvector, caching, and synchronization within a multicore chip organization. The authors demonstrate that UPCYCLE achieves day-zero software maturity and outperforms NVIDIA's A100 in both inference and training, consuming less power. Notably, UPCYCLE requires no new compiler or software stack innovations, offering full deep learning architecture coverage and adaptability for different workloads. The paper emphasizes the importance of considering software maturity as a critical design constraint when developing new architectures for deep learning. 


summary: This paper proposes a novel optical subspace neural network (OSNN) architecture for deep learning, which utilizes a compact butterfly-style photonic-electronic neural chip. Compared to conventional GEMM-based ONNs, the OSNN architecture achieves a 7x reduction in trainable optical components, leading to lower area cost and energy consumption. The chip features a hardware-aware training framework that minimizes device programming precision and enhances noise robustness. Experimental results demonstrate the effectiveness of the neural chip in image recognition tasks, achieving a 94.16% accuracy in handwritten digit recognition with 3-bit weight programming precision. 


summary: This paper introduces Restructurable Activation Networks (RANs), a new paradigm for deep network design that optimizes for hardware efficiency by manipulating the amount of non-linearity in the model. RANs use a hardware-aware search space and semi-automatic search algorithm to replace inefficient blocks with hardware-aware blocks. They also offer a training-free model scaling method that links network topology to expressivity. RANs achieve state-of-the-art results on ImageNet at different scales for various hardware, outperforming existing methods in terms of accuracy and Frames-Per-Second (FPS). For instance, RAN-e achieves similar accuracy to EfficientNet-Lite-B0 while improving FPS by 1.5x on Arm micro-NPUs, while RAN-i achieves up to 2x reduction in #MACs over ConvNexts with similar or better accuracy. 


summary: This paper investigates the intersection of deep learning and neuromorphic hardware architectures, focusing on biologically plausible learning algorithms that are tolerant to hardware nonidealities.  The authors explore the impact of hardware imperfections and quantization on algorithm performance, as well as how network topologies and algorithm design choices can scale latency, energy, and area consumption. They compare the performance of traditional Backpropagation and Direct Feedback Alignment algorithms on Compute-In-Memory (CIM) hardware, demonstrating that Direct Feedback Alignment achieves significant speedups while Backpropagation delivers the highest accuracy. This work offers valuable insights into the design of efficient and robust learning systems for neuromorphic hardware. 


summary: Approximate computing methods have shown great potential for deep learning due to their reduced hardware costs, making them suitable for inference tasks on power-constrained devices. However, the lack of training methods has limited their full potential. This paper discusses training methods for approximate hardware, demonstrating the need for specialized training and proposing methods to speed up training by up to 18X. The authors address the limitations of existing approaches and propose techniques that combine error injection with accurate modeling to maintain model accuracy while reducing training time. 


summary: Optical computing has emerged as a potential solution to the escalating demands of AI/ML workloads. However, existing implementations face challenges in scalability, footprint, power consumption, and integration within existing datacenter architectures. This paper proposes a scalable optical AI accelerator utilizing a coherent photonic crossbar architecture with phase change material (PCM) for on-chip weight storage. The design incorporates all critical circuit blocks, modeling based on measured performance in a 45nm monolithic silicon photonic process. A system-level analysis for Resnet-50V1.5 is presented, accounting for memory, array size, photonic losses, and peripheral energy consumption.  The proposed 128×128 architecture achieves comparable inference per second (IPS) to Nvidia A100 GPU with significantly lower power and area consumption. 


summary: A "technology lottery" describes a research idea or technology succeeding over others because it is suited to the available software and hardware, not necessarily because it is superior to alternative directions. The nascent field of Self-Driving Laboratories (SDL), particularly those implemented as Materials Acceleration Platforms (MAPs), is at risk of an analogous pitfall: the next logical step for building MAPs is to take existing lab equipment and workflows and mix in some AI and automation. This whitepaper argues that the same simulation and AI tools that will accelerate the search for new materials, as part of the MAPs research program, also make possible the design of fundamentally new computing mediums. We need not be constrained by existing biases in science, mechatronics, and general-purpose computing, but rather we can pursue new vectors of engineering physics with advances in cyber-physical learning and closed-loop, self-optimizing systems. This paper outlines a simulation-based MAP program to design computers that use physics itself to solve optimization problems. Such systems mitigate the hardware-software-substrate-user information losses present in every other class of MAPs and they perfect alignment between computing problems and computing mediums eliminating any technology lottery. This paper offers concrete steps toward early Physical Computing (PC) -MAP advances and the longer term cyber-physical R&D, which is expected to introduce a new era of innovative collaboration between materials researchers and computer scientists. 


summary: This webpage does not include an abstract.  The content is primarily a website header and a reference to the Simons Foundation and member institutions. 


summary: Deep Q-Network (DQN) marked a major milestone for reinforcement learning, demonstrating for the first time that human-level control policies could be learned directly from raw visual inputs via reward maximization. Even years after its introduction, DQN remains highly relevant to the research community since many of its innovations have been adopted by successor methods. Nevertheless, despite significant hardware advances in the interim, DQN's original Atari 2600 experiments remain costly to replicate in full. This poses an immense barrier to researchers who cannot afford state-of-the-art hardware or lack access to large-scale cloud computing resources. To facilitate improved access to deep reinforcement learning research, we introduce a DQN implementation that leverages a novel concurrent and synchronized execution framework designed to maximally utilize a heterogeneous CPU-GPU desktop system. With just one NVIDIA GeForce GTX 1080 GPU, our implementation reduces the training time of a 200-million-frame Atari experiment from 25 hours to just 9 hours. The ideas introduced in our paper should be generalizable to a large number of off-policy deep reinforcement learning methods. 


summary: Egocentric, multi-modal data as available on future augmented reality (AR) devices provides unique challenges and opportunities for machine perception. These future devices will need to be all-day wearable in a socially acceptable form-factor to support always available, context-aware and personalized AI applications. Our team at Meta Reality Labs Research built the Project Aria device, an egocentric, multi-modal data recording and streaming device with the goal to foster and accelerate research in this area. In this paper, we describe the Project Aria device hardware including its sensor configuration and the corresponding software tools that enable recording and processing of such data. 


summary: Accelerating deep model training and inference is crucial in practice. Existing deep learning frameworks usually concentrate on optimizing training speed and pay fewer attentions to inference-specific optimizations. We propose a hardware-aware optimization framework, namely Woodpecker-DL (WPK), to accelerate inference by taking advantage of multiple joint optimizations from the perspectives of graph optimization, automated searches, domain-specific language (DSL) compiler techniques and system-level exploration. In WPK, we investigated two new automated search approaches based on genetic algorithm and reinforcement learning, respectively, to hunt the best operator code configurations targeting specific hardware. A customized DSL compiler is further attached to these search algorithms to generate efficient codes. To create an optimized inference plan, WPK systematically explores high-speed operator implementations from third-party libraries besides our automatically generated codes and singles out the best implementation per operator for use. Extensive experiments demonstrated that on a Tesla P100 GPU, we can achieve the maximum speedup of 5.40 over cuDNN and 1.63 over TVM on individual convolution operators, and run up to 1.18 times faster than TensorRT for end-to-end model inference. * Equal contributions. 


summary: This paper introduces a new type of continuous-variable thermodynamic computer called the stochastic processing unit (SPU), which is built using RLC circuits on a printed circuit board. The SPU can be used for both sampling and linear algebra tasks, and the paper demonstrates its use in Gaussian sampling and matrix inversion, the latter being the first thermodynamic linear algebra experiment. The paper also explores the potential of the SPU for uncertainty quantification in neural network classification. The authors believe that scaling up the SPU could significantly accelerate various probabilistic AI applications. 


summary: We propose SemifreddoNets, a system of fixed-topology neural networks with partially frozen weights, optimized for efficient hardware implementation. SemifreddoNets freeze some parameters at each layer, replacing multipliers with fixed scalers, reducing silicon area, logic delay, and memory requirements. This tradeoff between cost and flexibility allows for configurable weights at different scales and levels of abstraction. Although fixing the topology and some weights limits flexibility, the efficiency benefits outweigh the advantages of a fully configurable model for many use cases. SemifreddoNets use repeatable blocks, enabling adjustable model complexity without hardware changes. The hardware implementation achieves up to an order of magnitude reduction in silicon area and power consumption compared to general-purpose accelerator implementations. 


summary: This webpage does not contain the abstract of the paper "A Hardware–Software Blueprint for Flexible Deep Learning Specialization." The webpage is a standard IEEE Xplore page with links to user accounts, purchase details, profile information, and help resources. 


summary: Designing efficient hybrid networks for diverse edge devices is challenging due to varying hardware designs, supported operations, and compilation optimizations. Current NAS methods often rely on fixed architecture search spaces and hardware-agnostic latency proxies, leading to inaccurate latency predictions. SCAN-Edge addresses these limitations with a unified NAS framework that searches for optimal combinations of self-attention, convolution, and activation, accommodating various edge devices.  SCAN-Edge uses a hardware-aware evolutionary algorithm to accelerate the search process. Experiments show that the resulting hybrid networks achieve the latency of MobileNetV2 for 224x224 input on different edge devices. 


summary: This paper proposes a specialized hardware architecture for accelerating recommender systems. By analyzing Facebook's Deep Learning Recommendation Model (DLRM), the paper quantifies the impact of hardware parameters, such as memory system design, collective communication latency, and interconnect topology, on system throughput. The authors argue that this "scale-in" approach can significantly boost recommender system throughput for both inference and training compared to existing AI platforms. They also identify limitations of current AI accelerators and hardware platforms based on their analysis of the DLRM workload. 


summary: This paper proposes a memristive neuromorphic hardware implementation for the actor-critic algorithm in reinforcement learning (RL).  A two-fold training procedure is introduced, including ex-situ pre-training and in-situ re-training, which significantly reduces the number of weight updates, making it suitable for efficient in-situ learning implementations. The authors demonstrate the effectiveness of their approach in a case study involving balancing an inverted pendulum. This study highlights the potential of memristor-based hardware neural networks for handling complex tasks through in-situ reinforcement learning. 


summary: Research on efficient vision backbones is moving towards models that combine convolutions and transformer blocks. This paper focuses on hardware efficiency, analyzing common modules and architectural choices for backbones in terms of throughput and latency, instead of the traditional MACs metric. The analysis leads to a recipe for hardware-efficient macro design and a new, slimmed-down version of MultiHead Self-Attention. Combining these designs, the authors propose a new family of hardware-efficient backbone networks called LowFormer. LowFormer shows significant speedup in throughput and latency while maintaining or improving accuracy compared to existing efficient backbones. The paper evaluates LowFormer on various hardware platforms (GPU, mobile GPU, ARM CPU) and demonstrates its benefits for downstream tasks like object detection and semantic segmentation. Code and models are available online. 


summary: ## Abstract:

This paper presents a method for training keyword spotting models that are optimized for both general-purpose and specialized hardware.  The authors use a hardware-aware training approach to improve efficiency and reduce latency, making keyword spotting more suitable for real-time applications. The research specifically addresses the challenges of deploying keyword spotting on resource-constrained devices like mobile phones and embedded systems. 


summary: With the increasing computational demands of neural networks, many hardware accelerators for the neural networks have been proposed. Such existing neural network accelerators often focus on popular neural network types such as convolutional neural networks (CNNs) and recurrent neural networks (RNNs); however, not much attention has been paid to attention mechanisms, an emerging neural network primitive that enables neural networks to retrieve most relevant information from a knowledge-base, external memory, or past states. The attention mechanism is widely adopted by many state-of-the-art neural networks for computer vision, natural language processing, and machine translation, and accounts for a large portion of total execution time. We observe today's practice of implementing this mechanism using matrix-vector multiplication is suboptimal as the attention mechanism is semantically a content-based search where a large portion of computations ends up not being used. Based on this observation, we design and architect A 3 , which accelerates attention mechanisms in neural networks with algorithmic approximation and hardware specialization. Our proposed accelerator achieves multiple orders of magnitude improvement in energy efficiency (performance/watt) as well as substantial speedup over the state-of-the-art conventional hardware. 


summary: The use of deep learning has grown at an exponential rate, leading to numerous specialized hardware and software systems. Prior work typically considers software optimizations and hardware architectures separately, limiting the exploration of the design space. This paper presents a hardware/software co-design approach using constrained Bayesian optimization to automatically identify desirable design points. The optimization framework leverages the constrained features of the design space, achieving energy-delay product improvements of up to 40% compared to hand-tuned state-of-the-art systems for various neural models. 


summary: Convolutional neural networks (CNN) are widely used in machine intelligence tasks, but are computationally intensive and energy consuming.  AdderNet, a novel minimalist hardware architecture, replaces convolution with adder kernels using only additions, significantly reducing complexity and energy consumption.  To further optimize energy efficiency, the paper explores low-bit quantization for AdderNet with a shared-scaling-factor method, and designs specific and general-purpose hardware accelerators.  Experimental results demonstrate high performance with int8/int16 quantization, leading to a significant reduction in resources.  Deployment on an FPGA platform shows notable improvements in speed, logic resource utilization, and power consumption compared to traditional CNNs.  AdderNet surpasses other competitors in performance, power consumption, hardware resource consumption, and network generalization capability, demonstrating its potential for high-performance, energy-efficient AI applications. 


summary: This paper proposes a hardware design for Bayesian deep networks, exploiting cycle-to-cycle variability in oxide-based Resistive Random Access Memories (RRAMs) for probabilistic sampling. Instead of viewing variability as a disadvantage, the authors leverage it to realize a probabilistic sampling function, reducing the need for costly CMOS Gaussian random number generators. The design integrates "In-Memory" crossbar architectures for energy-efficient hardware primitives, enabling a new paradigm for probabilistic Artificial Intelligence. While previous work has explored RRAM stochastic switching processes for neuromorphic algorithms, this paper specifically focuses on utilizing probability distributions derived from RRAM variability for deep learning applications, paving the way for more efficient and cost-effective probabilistic AI hardware. 


summary: This document is a metadata record for a research paper on Semantic Scholar. It provides the paper's title, authors, publication date, and citation count. However, it does not contain the paper's abstract. To access the abstract, you will need to find the full paper. 


summary: Multiplexed gradient descent (MGD) is a gradient descent framework designed to train analog or digital neural networks in hardware. MGD utilizes zero-order optimization techniques for online training of hardware neural networks. The authors demonstrate that MGD can train neural networks on modern machine learning datasets, including CIFAR-10 and Fashion-MNIST, and compare its performance to backpropagation. They conclude that these optimization techniques can train a network on emerging hardware platforms orders of magnitude faster than the wall-clock time of training via backpropagation on a standard GPU, even in the presence of imperfect weight updates or device-to-device variations in the hardware. They also discuss how MGD can be applied to existing hardware as part of chip-in-the-loop training, or integrated directly at the hardware level. 


summary: This paper explores how hardware selection, often overlooked in machine learning, can significantly impact fairness and model performance, especially in ML-as-a-service platforms where users lack control over hardware. The authors demonstrate that different hardware choices can worsen existing performance disparities across demographic groups due to variations in gradient flows and loss surfaces. The paper provides theoretical and empirical analyses to identify the underlying factors and proposes a strategy to mitigate hardware-induced performance imbalances. 


summary: Deep learning recommendation models (DLRMs) are used by Meta and are the single largest AI application in terms of infrastructure demand in its data-centers. This paper presents Neo, a software-hardware co-designed system for high-performance distributed training of large-scale DLRMs. Neo uses a novel 4D parallelism strategy that combines table-wise, row-wise, column-wise, and data parallelism for training massive embedding operators in DLRMs. Neo also enables extremely high-performance and memory-efficient embedding computations using hybrid kernel fusion, software-managed caching, and quality-preserving compression. Finally, Neo is paired with ZionEX, a new hardware platform co-designed with Neo's 4D parallelism for optimizing communications for large-scale DLRM training. Evaluation on 128 GPUs using 16 ZionEX nodes shows that Neo outperforms existing systems by up to 40× for training 12-trillion-parameter DLRM models deployed in production. 


summary: The number of parameters in deep neural networks (DNNs) is scaling at about 5× the rate of Moore's Law. To sustain this growth, photonic computing is a promising avenue, as it enables higher throughput in dominant general matrix-matrix multiplication (GEMM) operations in DNNs than their electrical counterpart. However, purely photonic systems face several challenges including lack of photonic memory and accumulation of noise. In this paper, we present an electrophotonic accelerator, ADEPT, which leverages a photonic computing unit for performing GEMM operations, a vectorized digital electronic ASIC for performing non-GEMM operations, and SRAM arrays for storing DNN parameters and activations. In contrast to prior works in photonic DNN accelerators, we adopt a system-level perspective and show that the gains while large are tempered relative to prior expectations. Our goal is to encourage architects to explore photonic technology in a more pragmatic way considering the system as a whole to understand its general applicability in accelerating today's DNNs. Our evaluation shows that ADEPT can provide, on average, 5.73× higher throughput per Watt compared to the traditional systolic arrays (SAs) in a full-system, and at least 6.8× and 2.5× better throughput per Watt, compared to state-of-the-art electronic and photonic accelerators, respectively. 


summary: Nonlinear model predictive control (NMPC) is a powerful control method, but it's computationally expensive. This paper presents hardware FPGA neural network controllers trained to mimic NMPC using supervised learning. These Neural Controllers (NCs) are implemented on low-cost embedded FPGA hardware, enabling high-frequency control of physical systems like a cartpole and an F1TENTH race car. The NCs achieve performance matching NMPC in simulation and outperform it in real-world scenarios due to faster control rates enabled by the quick FPGA NC inference. This research demonstrates kHz control rates for a physical cartpole and offloads control to the FPGA hardware on the F1TENTH car.  The code and hardware implementation are available at [link to GitHub repository]. 


summary: Computing platforms in autonomous vehicles rely heavily on fast, accurate, and reliable decision-making, requiring specialized hardware accelerators to meet the demands of perception and machine vision. This paper examines ML accelerators for autonomous driving, highlighting their architecture styles and application in machine vision use cases.  The authors discuss implications for AV development, offer recommendations for researchers and practitioners, and outline a trajectory for future research in this emerging field. 


summary: Analog neural network (NN) accelerators promise significant energy and time savings, but a major challenge is their susceptibility to static fabrication errors.  Current training methods for programmable photonic interferometer circuits, a leading analog NN platform, fail to produce networks that perform well in the presence of such errors. Existing hardware error correction techniques require individual retraining of each NN, place high demands on component quality, or introduce hardware overhead. This paper introduces a novel one-time error-aware training technique that addresses all three problems by producing robust NNs that match the performance of ideal hardware and can be directly transferred to any faulty photonic NN with hardware errors up to five times larger than current fabrication tolerances. This approach eliminates the need for individual training, reduces component quality requirements, and avoids adding hardware overhead, making it practical for large-scale deployment of analog NNs in edge settings. 


summary: Convolutional neural networks (CNNs) are typically trained using 16- or 32-bit floating-point (FP). Lower precision is often sufficient for inference, most commonly 8-bit integer values. However, recent research has shown that low-precision FP can be highly effective for inference. Low-precision FP can be implemented in hardware FPGA and ASIC accelerators, but existing processors do not, in general, support custom precision FP. We propose hardware optimized bit-sliced floating-point operators (HOBFLOPS), a method of generating efficient custom-precision emulated bitsliced software FP arithmetic. We generate custom-precision software FP routines using a hardware design flow. An FP unit generator creates high-level FP arithmetic hardware descriptions, and we use a standard hardware design flow to optimize and synthesize these designs into circuits. We provide standard cell libraries that match the bitwise operations on the target microprocessor architecture, and a custom code-generator to translate the resulting circuits to bitslice software equivalents. We exploit bitslice parallelism to create a very wide (32-512 element) vectorized CNN convolution. Experiments show that HOBFLOPS provides a fast approach to emulating custom, low-precision FP in software. We demonstrate implementing various widths of HOBFLOPS multiplier and adder in the multiply-accumulate (MAC) of a CNN convolution. The HOBFLOPS optimized C/C++ MAC performance of the convolution on Arm Neon, Intel AVX2, and AVX5

summary: This paper proposes a methodology to evaluate and compare the performance of efficient neural network building blocks for computer vision in a hardware-aware manner.  The comparison utilizes Pareto fronts based on randomly sampled networks from a design space to capture the accuracy/complexity trade-offs. This approach provides more insights into the relationship between hardware cost and accuracy compared to previous comparison methods.  The methodology is applied to analyze different building blocks and evaluate their performance on various embedded hardware platforms, highlighting the importance of benchmarking building blocks as a preselection step in neural network design. This approach demonstrates the potential for speeding up inference by up to a factor of 2× on specific hardware ML accelerators through the selection of appropriate building blocks. 


summary: Graph neural networks (GNNs) have shown impressive performance in handling non-Euclidean data. However, current GNN designs primarily focus on accuracy, neglecting resource constraints and real-time requirements of edge applications. This paper introduces HGNAS, a Hardware-aware Graph Neural Architecture Search framework designed for resource-limited edge devices. HGNAS leverages a multi-stage search strategy to explore optimal architectures within a few GPU hours, while achieving hardware awareness through a hardware performance predictor. This predictor balances GNN model accuracy and efficiency based on the targeted device's characteristics. Experimental results demonstrate that HGNAS achieves significant speedups (up to 10.6×) and peak memory reduction (88.2%) with minimal accuracy loss compared to DGCNN across various edge devices. 


summary: Convolutional neural networks (CNNs) have become the state-of-the-art in various AI tasks but their inference is computationally expensive. This work introduces HAPI, a new methodology for generating high-performance early-exit networks by co-optimising the placement of intermediate exits with the early-exit strategy during inference. HAPI proposes an efficient design space exploration algorithm to quickly traverse a large number of architectures and find the best design for a specific use case and hardware. Evaluations show that HAPI consistently outperforms other search methods and state-of-the-art early-exit schemes across latency budgets, achieving up to 5.11× speedup over lightweight models on embedded devices. 


summary: Modern consumer electronic devices often use deep neural networks for intelligent services.  This paper proposes an extension to the NNStreamer stream pipeline framework to support among-device AI, enabling the sharing of computing resources and hardware capabilities across devices of various vendors. The goal is to expand the use of on-device AI services, making them atomic, re-deployable, and shareable among connected devices. This work is part of the Linux Foundation (LF AI & Data) open source project and welcomes community contributions. 


summary: Deploying deep learning models in cloud clusters provides efficient and prompt inference services. These clusters usually have CPUs for input preprocessing and GPUs for forward computation. Recurrent neural networks (RNNs), essential for temporal inputs, have high inter-operator parallelism. Chrion optimizes RNN inference by collaboratively utilizing CPUs and GPUs. It formulates model deployment as an NP-hard scheduling problem on heterogeneous devices. Chrion preprocesses the model, partitions the graph to select execution devices, and performs forward computation in parallel on the CPU and GPU. Experiments show a 19.4% reduction in execution time (latency-optimal) and a 67.5% reduction in GPU memory footprint (memory-optimal) compared to GPU-only execution. 


summary: Customized hardware accelerators have been developed to provide improved performance and efficiency for DNN inference and training. However, the existing hardware accelerators may not always be suitable for handling various DNN models as their architecture paradigms and configuration tradeoffs are highly application-specific. It is important to benchmark the accelerator candidates in the earliest stage to gather comprehensive performance metrics and locate the potential bottlenecks. Further demands also emerge after benchmarking, which require adequate solutions to address the bottlenecks and improve the current designs for targeted workloads. To achieve these goals, in this paper, we leverage an automation tool called DNNExplorer [1] for benchmarking customized DNN hardware accelerators and exploring novel accelerator designs with improved performance and efficiency. Key features include (1) direct support to popular machine learning frameworks for DNN workload analysis and accurate analytical models for fast accelerator benchmarking; (2) a novel accelerator design paradigm with high-dimensional design space support and fine-grained adjustability to overcome the existing design drawbacks; and (3) a design space exploration (DSE) engine to generate optimized accelerators by considering targeted AI workloads and available hardware resources. Results show that accelerators adopting the proposed novel paradigm can deliver up to 4.2× higher throughput (GOP/s) than the state-of-the-art pipeline design in [2] and up to 2.0× improved efficiency than the recently published generic design in [3]) given the same DNN model and resource budgets. With DNNExplorer's benchmarking and exploration features, we

summary: DNN/Accelerator co-design has shown great potential in improving QoR and performance. Typical approaches separate the design flow into two-stage: (1) designing an application-specific DNN model with the highest accuracy; (2) building an accelerator considering the DNN specific characteristics. Though significant efforts have been dedicated to the improvement of DNN accuracy, it may fail in promising the highest composite score which combines the goals of accuracy and other hardware-related constraints (e.g., latency, energy efficiency) when building a specific neural network-based system. In this work, we present a single-stage automated framework, YOSO, aiming to generate the optimal solution of software-and-hardware that flexibly balances between the goal of accuracy, power, and QoS. YOSO jointly searches in the combined DNN and accelerator design spaces, which achieves a better composite score when facing a multiobjective design goal. As the search space is vast and it is costly to directly evaluate the accuracy and performance of the DNN and hardware architecture in design space search, we propose a cost-effective method to measure the accuracy and performance of solutions under consideration quickly. Compared with the two-stage method on the baseline systolic array accelerator and state-of-the-art dataset, we achieve 1.42x~2.29x energy reduction or 1.79x~3.07x latency reduction at the same level of precision, for different user-specified energy and

summary: The explosive growth of various types of big data and advances in AI technologies have catalyzed a new type of workload called multi-modal DNNs. These DNNs interpret and reason about information from multiple modalities, making them more applicable to real-world AI scenarios. Despite their importance, limited research has focused on understanding their characteristics and implications on current computing software/hardware platforms. Existing benchmarks either target uni-modal DNNs or focus on algorithm characteristics. To advance the understanding of multi-modal DNN workloads and facilitate related research, we present MM-Bench, an open-source, end-to-end benchmark suite consisting of real-world multi-modal DNN workloads with relevant performance metrics for evaluation. MM-Bench is used to conduct an in-depth analysis on the characteristics of multi-modal DNNs, demonstrating their unique characteristics of clear multi-stage execution, frequent synchronization, and high heterogeneity, which distinguish them from conventional uni-modal DNNs. This work aims to provide insights for future software/hardware design and optimization to underpin multi-modal DNNs on both cloud and edge computing platforms. 


summary: Widely popular transformer-based NLP models such as BERT and GPT have enormous capacity trending to billions of parameters. Current execution methods demand brute-force resources such as HBM devices and high-speed interconnectivity for data parallelism. In this paper, we introduce a new relay-style execution technique called L2L (layer-to-layer) where at any given moment, the device memory is primarily populated only with the executing layer(s)'s footprint. The model resides in the DRAM memory attached to either a CPU or an FPGA as an entity we call eager param-server (EPS). Unlike a traditional param-server, EPS transmits the model piecemeal to the devices thereby allowing it to perform other tasks in the background such as reduction and distributed optimization. To overcome the bandwidth issues of shuttling parameters to and from EPS, the model is executed a layer at a time across many micro-batches instead of the conventional method of minibatches over the whole model. In this paper, we explore a conservative version of L2L that is implemented on a modest Azure instance for BERT-Large running it with a batch size of 32 on a single V100 GPU using less than 8GB memory. Our results show a more stable learning curve, faster convergence, better accuracy, and 35% reduction in memory compared to the state-of-the-art baseline. Our method reproduces BERT results on any mid-level GPU that was hitherto not feasible. L2L

summary: This paper addresses the challenges of deploying machine learning workloads on edge embedded devices, which are characterized by limited compute and memory resources, tight power budgets, and real-time decision-making requirements. The authors propose a comprehensive design methodology for efficient DNN applications on embedded systems, including efficient DNN model designs, accelerator design and workload mapping technologies, and cross-stack optimization strategies. The paper discusses the challenges of deploying machine learning workloads on edge embedded devices, including the complexity of DNN models, the difficulty of mapping DNNs onto existing hardware, and the lack of efficient optimization strategies. 


summary: A key issue in system design is the lack of communication between hardware, software, and domain experts.  Recent research work shows progress in automatic HW/SW co-design flows of neural accelerators that seems to make this kind of communication obsolete. However, most real-world systems are a composition of multiple processing units, communication networks, and memories.  This position paper discusses possibilities for establishing a methodology for systems that include (reconfigurable) dedicated accelerators and outlines the central role that languages and tools play in the process.  


summary: ## Abstract:

Recently, a novel model named Kolmogorov-Arnold Networks (KAN) has been proposed with the potential to achieve the functionality of traditional deep neural networks (DNNs) using orders of magnitude fewer parameters by parameterized B-spline functions with trainable coefficients. However, the B-spline functions in KAN present new challenges for hardware acceleration. Evaluating the B-spline functions can be performed by using look-up tables (LUTs) to directly map the B-spline functions, thereby reducing computational resource requirements. However, this method still requires substantial circuit resources (LUTs, MUXs, decoders, etc.). For the first time, this paper employs an algorithm-hardware co-design methodology to accelerate KAN. The proposed algorithm-level techniques include Alignment-Symmetry and PowerGap KAN hardware aware quantization, KAN sparsity aware mapping strategy, and circuit-level techniques include N:1 Time Modulation Dynamic Voltage input generator with analog-CIM (ACIM) circuits. The impact of non-ideal effects, such as partial sum errors caused by the process variations, has been evaluated with the statistics measured from the TSMC 22nm RRAM-ACIM prototype chips. With the best searched hyperparameters of KAN and the optimized circuits implemented in 22 nm node, we can reduce hardware area by 41.78x, energy by 77.97x with 3.03% accuracy boost compared to the traditional DNN hardware. 


summary: Distributed deep learning training requires careful consideration of hardware architecture and device placement strategies. This paper introduces PHAZE, a novel approach that co-optimizes both aspects, achieving higher throughput for large language models compared to existing methods. PHAZE leverages tensor and vector units, memory configurations, and dynamic programming to find optimal operator scheduling and device placement strategies. It also considers microbatch size, recomputation, and activation stashing to balance memory usage and storage requirements. The entire source code for PHAZE is available on GitHub. 


summary: The paper presents RHNAS, a novel method for jointly optimizing neural network architecture and hardware accelerators. RHNAS combines reinforcement learning for hardware optimization with differentiable neural architecture search, resulting in realizable designs with improved latency and energy efficiency. The authors highlight the challenges of fully differentiable co-design methods, which fail to account for nonsynthesizable (invalid) designs in hardware search spaces. RHNAS addresses this limitation by enabling the exploration of configurable hardware accelerators with arbitrary neural network search spaces, ultimately achieving significant performance gains over default hardware accelerator designs. 


summary: Neural networks are powerful tools for analyzing big data, but traditional CPUs cannot achieve the desired performance or energy efficiency for these applications. While GPGPUs offer general purpose and high throughput, they lack the energy efficiency needed for data reuse. ASIC accelerators excel in performance and energy efficiency but have limited use cases. CISC accelerators attempt to achieve both general purpose and high energy efficiency by decomposing NN applications into simple instructions, but they fail to achieve the same level of data reuse optimization as ASIC accelerators.  This paper proposes RISC-NN, a novel many-core RISC-based NN accelerator that achieves high expressiveness, parallelism, programmability, and low control-hardware costs. It can implement all the necessary instructions of state-of-the-art CISC accelerators, while also achieving advanced optimization like multiple-level data reuse and support for Sparse NN applications. Experimental results show that RISC-NN outperforms Nvidia TITAN Xp GPGPU by an average of 11.88x, and outperforms CISC-based TPU by an average of 1.29x, 8.37x, and 21.71x for CNN, MLP, and LSTM applications, respectively. Additionally, RISC-NN achieves further performance improvements and energy reductions when applied to Sparse NN applications. 


summary: Embodied AI robots have the potential to significantly improve human life and manufacturing, and progress in using large language models (LLMs) to control robots depends heavily on efficient computing systems. Current computing systems for embodied AI robots are designed with a frame-based approach, resulting in high latency and energy consumption. Corki is a novel algorithm-architecture co-design framework for real-time embodied AI robot control that aims to address this issue. Corki decouples LLM inference, robotic control, and data communication to predict trajectories for the near future, thus reducing LLM inference frequency. This is coupled with hardware that accelerates trajectory conversion into torque signals for robot control and a parallel execution pipeline for data communication and computation.  As a result, Corki significantly reduces LLM inference frequency (up to 8.0x), leading to a speed-up of up to 3.6x and a success rate improvement of up to 17.3%. The code for re-implementation is available. 


summary: This paper proposes STAR, a new architecture for attention models using RRAM crossbars. STAR addresses the efficiency bottleneck of frequent softmax operations by utilizing a dedicated RRAM-based softmax engine and a fine-grained global pipeline.  The paper demonstrates that this approach leads to significant performance improvements over both GPUs and existing RRAM-based attention accelerators, achieving up to 30.63x and 1.31x efficiency gains, respectively. 
    ''',
    llm_config=config_list_custom[0],
)
scientist_ai_hardware_engineer.register_model_client(model_client_cls=AI21JambaModelClient)


"""
GRANT WRITERS
"""


planner = AssistantAgent(
   name="planner",
   system_message = '''Planner. You are a helpful AI assistant. Your task is to suggest a comprehensive plan to write a scientific grant application.

Explain the Plan: Begin by providing a clear overview of the plan.
Break Down the Plan: For each part of the plan, explain the reasoning behind it, and describe the specific actions that need to be taken.
No Execution: Your role is strictly to suggest the plan. Do not take any actions to execute it.
No Tool Call: You are not allowed to call any Tool or function yourself. 

''',
   llm_config=config_list_custom[0],
   description='Who can suggest a step-by-step plan to solve the task by breaking down the task into simpler sub-tasks.',
)
planner.register_model_client(model_client_cls=AI21JambaModelClient)

# assistant = AssistantAgent(
#    name="assistant",
#    system_message = '''You are a helpful AI assistant.
  
# Your role is to call the appropriate tools and functions as suggested in the plan. You act as an intermediary between the planner's suggested plan and the execution of specific tasks using the available tools. You ensure that the correct parameters are passed to each tool and that the results are accurately reported back to the team.


# Return "TERMINATE" in the end when the task is over.
# ''',
#    llm_config=config_list_custom[0],
#    description='''An assistant who calls the tools and functions as needed and returns the results. Tools include "rate_novelty_feasibility" and "generate_path".''',
# )
# assistant.register_model_client(model_client_cls=AI21JambaModelClient)

scientist = AssistantAgent(
   name="scientist",
   system_message = '''scientist. You must follow the plan from the planner.
  
You are a sophisticated scientist trained in scientific research, innovation, and grant writing.
  
Your task is to synthesize a grant proposal for a novel research idea with initial key aspects-hypothesis, objectives, methodology, novelty, ethics, budget, and comparison - BASED ON the input from the three expert scientists before you. Synthesize their outputs and propose a novel concept that combines their ideas.

Be as quantitative as possible and include details such as numbers, sequences, or mathematical formulas.


Your response should include the following SEVEN keys in great detail:


"hypothesis" clearly delineates the hypothesis at the basis for the proposed research question. The hypothesis should be well-defined, has novelty, is feasible, has a well-defined purpose and clear components. Your hypothesis should be as detailed as possible.


"objectives" describes the expected findings or impact of the research. Be quantitative and include numbers, functions, theories, etc.


"methodology" outlines the specific algorithms, techniques, datasets, and evaluation metrics used in the study, providing a detailed explanation of how the research was conducted to ensure transparency, reproducibility, and the soundness of the results achieved.


"novelty" should discuss novel aspects of the proposed idea, specifically highlighting how this advances over existing knowledge and technology.


"ethics" should discuss the ethical and potential societal implications of the proposed idea or concept(s), if any.


"budget" should provide a detailed account of the budget required for project for the grant application. Be comprehensive and provide quantitative estimates.


"comparison" should provide a detailed comparison with other approaches, technologies or scientific concepts. Be detailed and quantitative.


Ensure your scientific proposal is both innovative and grounded in logical reasoning, capable of advancing our understanding or application of the concepts provided.


Here is an example structure for your response, in the following order:


{{
 "1- hypothesis": "...",
 "2- objectives": "...",
 "3- methodology": "...",
 "4- novelty": "...",
 "5- ethics": "...",
 "6- budget": "...",
 "7- comparison ": "..."
}}


Remember, the value of your response lies in scientific discovery, new avenues of scientific inquiry, and potential technological breakthroughs, with detailed and solid reasoning.


Further Instructions:
Perform only the tasks assigned to you in the plan; do not undertake tasks assigned to other agents.
Additionally, do not execute any functions or tools.
''',
   llm_config=config_list_custom[0],
   description='I can craft the grant research proposal with key aspects.',
)
scientist.register_model_client(model_client_cls=AI21JambaModelClient)


hypothesis_agent = AssistantAgent(
   name="hypothesis_agent",
   system_message = '''hypothesis_agent. Carefully expand on the ```{hypothesis}```  of the research proposal.


Critically assess the original content and improve on it. \
Add more specifics, quantitive scientific information (such as mathematical formulas, numbers, sequences, scientific theory, functions, etc.), \
rationale, and step-by-step reasoning. When possible, comment on specific modeling and simulation techniques, experimental methods, or particular analyses.


Start by carefully assessing this initial draft from the perspective of a peer-reviewer whose task it is to critically assess and improve the science of the following:


<hypothesis>
where <hypothesis> is the hypothesis aspect of the research proposal. 


Do not add any introductory phrases. Your response begins with your response, with a heading: ### Expanded ...
''',
   llm_config=config_list_custom[0],
   description='''I can expand the "hypothesis" aspect of the research proposal crafted by any of the scientists.''',
)
hypothesis_agent.register_model_client(model_client_cls=AI21JambaModelClient)


objective_agent = AssistantAgent(
   name="objective_agent",
   system_message = '''objective_agent. Carefully expand on the ```{objective}``` of the research proposal developed by the scientists.


Critically assess the original content and improve on it. \
Add more specifics, quantitive scientific information (such as mathematical formulas, numbers, sequences, scientific theory, functions, etc.), \
rationale, and step-by-step reasoning. When possible, comment on specific modeling and simulation techniques, experimental methods, or particular analyses.


Start by carefully assessing this initial draft from the perspective of a peer-reviewer whose task it is to critically assess and improve the science of the following:


<outcome>
where <outcome> is the outcome aspect of the research proposal. 


Do not add any introductory phrases. Your response begins with your response, with a heading: ### Expanded ...
''',
   llm_config=config_list_custom[0],
   description='''I can expand the "objective" aspect of the research proposal crafted by the "scientist".''',
)
objective_agent.register_model_client(model_client_cls=AI21JambaModelClient)


methodology_agent = AssistantAgent(
   name="methodology_agent",
   system_message = '''methodology_agent. Carefully expand on this particular aspect: ```{methodology}``` of the research proposal.


Critically assess the original content and improve on it. \
Add more specifics, quantitive scientific information (such as chemical formulas, numbers, sequences, processing conditions, etc.), \
rationale, and step-by-step reasoning. When possible, comment on specific modeling and simulation techniques, experimental methods, or particular analyses.


Start by carefully assessing this initial draft from the perspective of a peer-reviewer whose task it is to critically assess and improve the science of the following:


<methodology>
where <methodology> is the mechanism aspect of the research proposal. 


Do not add any introductory phrases. Your response begins with your response, with a heading: ### Expanded ...
''',
   llm_config=config_list_custom[0],
   description='''I can expand the "methodology" aspect of the research proposal crafted by the "scientist"''',
)
methodology_agent.register_model_client(model_client_cls=AI21JambaModelClient)


ethics_agent = AssistantAgent(
   name="ethics_agent",
   system_message = '''ethics_agent. Carefully expand on this particular aspect: ```{ethics}``` of the research proposal.


Critically assess the original content and improve on it. \
Add more specifics, quantitive scientific information (such as chemical formulas, numbers, sequences, processing conditions, microstructures, etc.), \
rationale, and step-by-step reasoning. When possible, comment on specific modeling and simulation techniques, experimental methods, or particular analyses.


Start by carefully assessing this initial draft from the perspective of a peer-reviewer whose task it is to critically assess and improve the science of the following:


<ethics>
where <ethics> is the design_principles aspect of the research proposal. 


Do not add any introductory phrases. Your response begins with your response, with a heading: ### Expanded ...
''',
   llm_config=config_list_custom[0],
   description='''I can expand the "ethics" aspect of the research proposal crafted by the "scientist".''',
)
ethics_agent.register_model_client(model_client_cls=AI21JambaModelClient)


comparison_agent = AssistantAgent(
   name="comparison_agent",
   system_message = '''comparison_agent. Carefully expand on this particular aspect: ```{comparison}``` of the research proposal.


Critically assess the original content and improve on it. \
Add more specifics, quantitive scientific information (such as chemical formulas, numbers, sequences, processing conditions, microstructures, etc.), \
rationale, and step-by-step reasoning. When possible, comment on specific modeling and simulation techniques, experimental methods, or particular analyses.


Start by carefully assessing this initial draft from the perspective of a peer-reviewer whose task it is to critically assess and improve the science of the following:


<comparison>
where <comparison> is the comparison aspect of the research proposal. 


Do not add any introductory phrases. Your response begins with your response, with a heading: ### Expanded ...
''',
   llm_config=config_list_custom[0],
   description='''I can expand the "comparison" aspect of the research proposal crafted by the "scientist".''',
)
comparison_agent.register_model_client(model_client_cls=AI21JambaModelClient)


novelty_agent = AssistantAgent(
   name="novelty_agent",
   system_message = '''novelty_agent. Carefully expand on this particular aspect: ```{novelty}``` of the research proposal.


Critically assess the original content and improve on it. \
Add more specifics, quantitive scientific information (such as chemical formulas, numbers, sequences, processing conditions, microstructures, etc.), \
rationale, and step-by-step reasoning. When possible, comment on specific modeling and simulation techniques, experimental methods, or particular analyses.


Start by carefully assessing this initial draft from the perspective of a peer-reviewer whose task it is to critically assess and improve the science of the following:


<novelty>
where <novelty> is the novelty aspect of the research proposal. 


Do not add any introductory phrases. Your response begins with your response, with a heading: ### Expanded ...
''',
   llm_config=config_list_custom[0],
   description='''I can expand the "novelty" aspect of the research proposal crafted by the "scientist".''',
)
novelty_agent.register_model_client(model_client_cls=AI21JambaModelClient)

budget_agent = AssistantAgent(
   name="budget_agent",
   system_message = '''budget_agent. Carefully expand on this particular aspect: ```{budget}``` of the research proposal.


Critically assess the original content and improve on it. \
Add more specifics, quantitive scientific information (such as chemical formulas, numbers, sequences, processing conditions, microstructures, etc.), \
rationale, and step-by-step reasoning. When possible, comment on specific modeling and simulation techniques, experimental methods, or particular analyses.


Start by carefully assessing this initial draft from the perspective of a peer-reviewer whose task it is to critically assess and improve the science of the following:


<budget>
where <budget> is the novelty aspect of the research proposal. 


Do not add any introductory phrases. Your response begins with your response, with a heading: ### Expanded ...
''',
   llm_config=config_list_custom[0],
   description='''I can expand the "budget" aspect of the research proposal crafted by the "scientist".''',
)
budget_agent.register_model_client(model_client_cls=AI21JambaModelClient)


critic_agent = AssistantAgent(
   name="critic_agent",
   system_message = '''critic_agent. You are a helpful AI agent who provides accurate, detailed and valuable responses.


You read the whole proposal with all its details and expanded aspects and provide:


(1) a summary of the document (in one paragraph, but including sufficient detail such as mechanisms, \
related technologies, models and experiments, methods to be used, and so on), \


(2) a thorough critical scientific review with strengths and weaknesses, and suggested improvements. Include logical reasoning and scientific approaches.


Next, from within this document,


(1) identify the single most impactful scientific question that can be tackled with molecular modeling. \
\n\nOutline key steps to set up and conduct such modeling and simulation, with details and include unique aspects of the planned work.


(2) identify the single most impactful scientific question that can be tackled with synthetic biology. \
\n\nOutline key steps to set up and conduct such experimental work, with details and include unique aspects of the planned work.'


Important Note:
***You do not rate Novelty and Feasibility. You are not to rate the novelty and feasibility.***''',
   llm_config=config_list_custom[0],
   description='''I can summarizes, critique, and suggest improvements after all seven aspects of the proposal have been expanded by the agents.''',
)
critic_agent.register_model_client(model_client_cls=AI21JambaModelClient)


"""
INITIATE GROUP CHAT
"""

groupchat = autogen.GroupChat(
   agents=[planner, scientist_computer_vision_engineer, scientist_ai_language_models, scientist_ai_hardware_engineer, scientist, hypothesis_agent, objective_agent, methodology_agent, novelty_agent, ethics_agent, budget_agent, critic_agent],
     messages=[],
     max_round=50,
     admin_name='user',
     send_introductions=True,
     allow_repeat_speaker=True,
   speaker_selection_method='round_robin', #change to auto later
)
manager = autogen.GroupChatManager(groupchat=groupchat,
                                  llm_config=config_list_custom[0],
                                  system_message='moderator. You are a helpful AI assistant. Your task is to moderate an academic discussion between scientists who are experts in distinct different fields and select the next speaker from the group of scientists that would be good to speak based on the discussion.')


task = "Propose a novel neural network architecture that draws inspiration from multiple disciplines."

society_of_mind_agent = SocietyOfMindAgent(
   "society_of_mind",
   chat_manager=manager,
   llm_config=config_list_custom[0],
)

society_of_mind_agent.register_model_client(model_client_cls=AI21JambaModelClient)

user_proxy = autogen.UserProxyAgent(
   "user_proxy",
   human_input_mode="NEVER",
   code_execution_config=False,
   default_auto_reply="",
   is_termination_msg=lambda x: True,
)

res = user_proxy.initiate_chat(society_of_mind_agent, message=task)


# Save data
formatted_text = ""
formatted_text_summary = ""
for i in range(len(res.chat_history)):
    try:
        formatted_text += f'''{res.chat_history[i]['tool_calls'][0]['function']['name']}-{res.chat_history[1]['tool_calls'][0]['function']['arguments']}\n\n'''
    except:
        if i==0:
            formatted_text += '### ' + f'''{res.chat_history[i]['content']}\n\n'''
        else:
            formatted_text += f'''{res.chat_history[i]['content']}\n\n'''
            if res.search("Summary of the Initial Research Hypothesis", f'''{res.chat_history[i]['content']}'''):
                formatted_text_summary += f'''{res.chat_history[i]['content']}'''

text_markdown = Markdown(formatted_text)

markdown_to_pdf(formatted_text, 'output_research')


# """
# USER INTERFACE"""

# # Define frontend using Panel
# pn.extension(design="material")

# # Global variable to manage input
# input_future = None
# initiate_chat_task_created = False

# # Define callback function for chat input
# async def callback(contents: str, user: str, instance: pn.chat.ChatInterface):
#     global initiate_chat_task_created
#     global input_future

#     if not initiate_chat_task_created:
#         asyncio.create_task(delayed_initiate_chat(user_proxy, assistant, contents))
#     else:
#         if input_future and not input_future.done():
#             input_future.set_result(contents)
#         else:
#             print("There is currently no input being awaited.")

# # Chat interface initialization
# chat_interface = pn.chat.ChatInterface(callback=callback)
# chat_interface.send("Send a message to the Neuroscience Assistant!", user="System", respond=False)

# # Function to print messages
# def print_messages(recipient, messages, sender, config):
#     content = messages[-1]['content']
#     chat_interface.send(content, user=recipient.name, avatar="🧠", respond=False)
#     return False, None  # Ensure the agent communication flow continues

# # Register the message handler for the assistant
# user_proxy.register_reply([AssistantAgent, None], reply_func=print_messages, config={"callback": None})

# # Async task to delay the initiation of the chat
# async def delayed_initiate_chat(agent, recipient, message):
#     global initiate_chat_task_created
#     initiate_chat_task_created = True
#     await asyncio.sleep(2)
#     await agent.a_initiate_chat(recipient, message=message)

# # Serve the chat interface as the Panel app
# chat_interface.servable()

# # Start a conversation with the scientist agent (Initial prompt)