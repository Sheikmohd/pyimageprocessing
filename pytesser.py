"""OCR in Python using the Tesseract engine from Google
http://code.google.com/p/pytesser/
by Michael J.T. O'Kelly
V 0.0.1, 3/10/07"""

from PIL import Image
import subprocess

import util
import errors

tesseract_exe_name = 'tesseract' # Name of executable to be called at command line
scratch_image_name = "temp.bmp" # This file must be .bmp or other Tesseract-compatible format
scratch_text_name_root = "temp" # Leave out the .txt extension
cleanup_scratch_flag = True  # Temporary files cleaned up after OCR operation

def call_tesseract_micr(input_filename, output_filename):
	"""Calls external tesseract.exe on input file (restrictions on types),
	outputting output_filename+'txt'"""
	print "called call_tesseract_micr"
	args = [tesseract_exe_name, "-l","mcr",input_filename, output_filename]
	proc = subprocess.Popen(args)
	retcode = proc.wait()
	if retcode!=0:
		errors.check_for_errors()

def call_tesseract(input_filename, output_filename):
	"""Calls external tesseract.exe on input file (restrictions on types),
	outputting output_filename+'txt'"""
	print "called call_tesseract"

	args = [tesseract_exe_name, input_filename, output_filename]
	proc = subprocess.Popen(args)
	retcode = proc.wait()
	if retcode!=0:
		errors.check_for_errors()

def image_to_string(im, cleanup = cleanup_scratch_flag):
	"""Converts im to file, applies tesseract, and fetches resulting text.
	If cleanup=True, delete scratch files after operation."""
	print "image_to_string"
	try:
		util.image_to_scratch(im, scratch_image_name)
		if(filename.contains("micr")):
			call_tesseract_micr(scratch_image_name, scratch_text_name_root)
		else:
			call_tesseract(scratch_image_name, scratch_text_name_root)

		text = util.retrieve_text(scratch_text_name_root)
	finally:
		if cleanup:
			util.perform_cleanup(scratch_image_name, scratch_text_name_root)
	return text

def image_file_to_string(filename, cleanup = cleanup_scratch_flag, graceful_errors=True):
	"""Applies tesseract to filename; or, if image is incompatible and graceful_errors=True,
	converts to compatible format and then applies tesseract.  Fetches resulting text.
	If cleanup=True, delete scratch files after operation."""
	print "image_file_to_string",filename
	try:
		try:
			if "micr" in filename:
				print "image_file_to_string micr"
				call_tesseract_micr(filename, scratch_text_name_root)
			else:
				print "else of image_file_to_string micr"
				call_tesseract(filename, scratch_text_name_root)

			text = util.retrieve_text(scratch_text_name_root)
		except errors.Tesser_General_Exception:
			print "in except of image_file_to_string",errors
			if graceful_errors:
				im = Image.open(filename)
				text = image_to_string(im, cleanup)
			else:
				raise
	except Exception as e:
			print "errors",e
	finally:
		if cleanup:
			util.perform_cleanup(scratch_image_name, scratch_text_name_root)
	return text