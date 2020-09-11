from Parsers import HpoParser

array = [descendant for descendant in HpoParser().get_descendants('HP:0000118')]
# array1 = [descendant for descendant in HpoParser().get_descendants('HP:0000001')]

print(len(array))

# diff = list(set(array1)-set(array))
# print(diff)

# diff2 = ['HP:0032540', 'HP:0032316', 'HP:0025296', 'HP:0025301', 'HP:0001450', 'HP:0030650', 'HP:0012823', 'HP:0025211', 'HP:0025219', 'HP:0020139', 'HP:0030647', 'HP:0012831', 'HP:0003621', 'HP:0012838', 'HP:0025285', 'HP:0032525', 'HP:0025307', 'HP:0025305', 'HP:0031796', 'HP:0032535', 'HP:0040280', 'HP:0032370', 'HP:0031915', 'HP:0500260', 'HP:0032443', 'HP:0032365', 'HP:0001699', 'HP:0032440', 'HP:0012832', 'HP:0030651', 'HP:0032534', 'HP:0025292', 'HP:0025286', 'HP:0025209', 'HP:0030648', 'HP:0032467', 'HP:0030646', 'HP:0012275', 'HP:0010985', 'HP:0025227', 'HP:0025280', 'HP:0011462', 'HP:0032224', 'HP:0011009', 'HP:0025208', 'HP:0025153', 'HP:0011463', 'HP:0025281', 'HP:0025222', 'HP:0025215', 'HP:0032375', 'HP:0003831', 'HP:0012839', 'HP:0032539', 'HP:0032319', 'HP:0003743', 'HP:0025216', 'HP:0032500', 'HP:0025290', 'HP:0025213', 'HP:0500261', 'HP:0003581', 'HP:0031797', 'HP:0040282', 'HP:0001522', 'HP:0040006', 'HP:0001444', 'HP:0003819', 'HP:0000007', 'HP:0001423', 'HP:0020140', 'HP:0025308', 'HP:0012835', 'HP:0003679', 'HP:0025295', 'HP:0030674', 'HP:0025214', 'HP:0025225', 'HP:0012825', 'HP:0032522', 'HP:0012829', 'HP:0032223', 'HP:0012828', 'HP:0410401', 'HP:0031914', 'HP:0010984', 'HP:0025256', 'HP:0000118', 'HP:0011461', 'HP:0001425', 'HP:0012827', 'HP:0025206', 'HP:0010982', 'HP:0001466', 'HP:0025352', 'HP:0025303', 'HP:0025282', 'HP:0025223', 'HP:0003828', 'HP:0025205', 'HP:0003678', 'HP:0012824', 'HP:0025293', 'HP:0003812', 'HP:0032503', 'HP:0011460', 'HP:0032322', 'HP:0031375', 'HP:0025224', 'HP:0012837', 'HP:0032542', 'HP:0032557', 'HP:0012833', 'HP:0001427', 'HP:0003587', 'HP:0025218', 'HP:0011421', 'HP:0025306', 'HP:0020121', 'HP:0032502', 'HP:0003680', 'HP:0025210', 'HP:0001442', 'HP:0001417', 'HP:0032373', 'HP:0025212', 'HP:0025229', 'HP:0031450', 'HP:0025294', 'HP:0032444', 'HP:0025220', 'HP:0025284', 'HP:0012274', 'HP:0003682', 'HP:0003811', 'HP:0025257', 'HP:0040281', 'HP:0003596', 'HP:0025228', 'HP:0012834', 'HP:0025297', 'HP:0032318', 'HP:0000005', 'HP:0012830', 'HP:0020138', 'HP:0045090', 'HP:0003745', 'HP:0031362', 'HP:0025334', 'HP:0033032', 'HP:0003829', 'HP:0001428', 'HP:0011420', 'HP:0100613', 'HP:0025283', 'HP:0025226', 'HP:0011011', 'HP:0032320', 'HP:0030645', 'HP:0001419', 'HP:0003744', 'HP:0025279', 'HP:0032317', 'HP:0025377', 'HP:0025207', 'HP:0003584', 'HP:0025275', 'HP:0020034', 'HP:0410280', 'HP:0032113', 'HP:0003623', 'HP:0025217', 'HP:0011008', 'HP:0040279', 'HP:0003593', 'HP:0032544', 'HP:0032468', 'HP:0012840', 'HP:0031167', 'HP:0003674', 'HP:0045089', 'HP:0003677', 'HP:0000006', 'HP:0032321', 'HP:0032384', 'HP:0045088', 'HP:0025291', 'HP:0001426', 'HP:0025315', 'HP:0025255', 'HP:0032383', 'HP:0040285', 'HP:0003577', 'HP:0032441', 'HP:0032526', 'HP:0031135', 'HP:0032382', 'HP:0025287', 'HP:0025254', 'HP:0003676', 'HP:0001470', 'HP:0032501', 'HP:0040283', 'HP:0012826', 'HP:0032374', 'HP:0003826', 'HP:0025204', 'HP:0040284', 'HP:0032442', 'HP:0030649', 'HP:0025304', 'HP:0001452', 'HP:0025302', 'HP:0012836', 'HP:0010983', 'HP:0001475', 'HP:0025221', 'HP:0011010']
# print(len(diff2))
# from Common import utils
#
# translator = utils.load_object('./_data/results/experiment_16_object.pkl')
# print(translator)


# print(translator['id2name'])
#
# objeto = utils.load_object('./_data/walks/walks.pkl')
#
# for i in objeto:
#     if i[0] == '8317':
#         print([translator['id2name'][int(e)] for e in i])

# objeto = utils.load_object('./_data/patients/decipher_patient_sims.pkl')
# print(objeto)

# from Validation import ROC_AUC_EXPERIMENT
#
# ROC_AUC_EXPERIMENT('orpha').plot_it()
# import json
#
# with open('_emu/emu-decipher-sample.json', 'r') as file:
#     decipher = json.load(file)
#
# with open('_emu/emu-orpha-sample.json', 'r') as file:
#     orpha = json.load(file)
#
# orpha.update(decipher)
#
# with open('_emu/emu-all-sample.json', 'w') as file:
#     json.dump(orpha, file, indent=2)
