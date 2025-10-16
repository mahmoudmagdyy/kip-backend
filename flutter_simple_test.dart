import 'dart:io';
import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:image_picker/image_picker.dart';

/// Simple test example for creating a service with image upload
class SimpleServiceTest extends StatefulWidget {
  @override
  _SimpleServiceTestState createState() => _SimpleServiceTestState();
}

class _SimpleServiceTestState extends State<SimpleServiceTest> {
  File? _selectedImage;
  bool _isLoading = false;
  String _result = '';

  // Replace with your actual API URL
  static const String API_URL = 'http://your-api-domain.com/api/dashboard/services/create/';

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Service Creation Test')),
      body: Padding(
        padding: EdgeInsets.all(16),
        child: Column(
          children: [
            // Image Preview
            Container(
              height: 200,
              width: double.infinity,
              decoration: BoxDecoration(
                border: Border.all(color: Colors.grey),
                borderRadius: BorderRadius.circular(8),
              ),
              child: _selectedImage == null
                  ? Center(child: Text('No image selected'))
                  : Image.file(_selectedImage!, fit: BoxFit.cover),
            ),
            SizedBox(height: 16),

            // Select Image Button
            ElevatedButton(
              onPressed: _pickImage,
              child: Text('Select Image'),
            ),
            SizedBox(height: 16),

            // Create Service Button
            ElevatedButton(
              onPressed: _isLoading ? null : _createService,
              child: _isLoading 
                  ? CircularProgressIndicator() 
                  : Text('Create Service'),
            ),
            SizedBox(height: 16),

            // Result Display
            if (_result.isNotEmpty)
              Expanded(
                child: Container(
                  width: double.infinity,
                  padding: EdgeInsets.all(12),
                  decoration: BoxDecoration(
                    color: Colors.grey[100],
                    borderRadius: BorderRadius.circular(8),
                  ),
                  child: SingleChildScrollView(
                    child: Text(
                      _result,
                      style: TextStyle(fontFamily: 'monospace'),
                    ),
                  ),
                ),
              ),
          ],
        ),
      ),
    );
  }

  Future<void> _pickImage() async {
    try {
      final ImagePicker picker = ImagePicker();
      final XFile? image = await picker.pickImage(
        source: ImageSource.gallery,
        maxWidth: 1024,
        maxHeight: 1024,
        imageQuality: 85,
      );
      
      if (image != null) {
        setState(() {
          _selectedImage = File(image.path);
        });
      }
    } catch (e) {
      setState(() {
        _result = 'Error picking image: $e';
      });
    }
  }

  Future<void> _createService() async {
    if (_selectedImage == null) {
      setState(() {
        _result = 'Please select an image first';
      });
      return;
    }

    setState(() {
      _isLoading = true;
      _result = 'Creating service...';
    });

    try {
      // Create multipart request
      var request = http.MultipartRequest('POST', Uri.parse(API_URL));
      
      // Add required form fields
      request.fields['title_ar'] = 'خدمة التصميم';
      request.fields['title_en'] = 'Design Service';
      request.fields['description_ar'] = 'وصف الخدمة بالعربية';
      request.fields['description_en'] = 'Service description in English';
      request.fields['is_active'] = 'true';
      request.fields['order'] = '0';

      // Add image file
      request.files.add(
        await http.MultipartFile.fromPath(
          'image',
          _selectedImage!.path,
          filename: 'service_image.jpg',
        ),
      );

      // Send request
      var streamedResponse = await request.send();
      var response = await http.Response.fromStream(streamedResponse);

      setState(() {
        _result = '''
Status Code: ${response.statusCode}
Response Body:
${response.body}
        ''';
      });

    } catch (e) {
      setState(() {
        _result = 'Error: $e';
      });
    } finally {
      setState(() {
        _isLoading = false;
      });
    }
  }
}

void main() {
  runApp(MaterialApp(
    home: SimpleServiceTest(),
  ));
}
